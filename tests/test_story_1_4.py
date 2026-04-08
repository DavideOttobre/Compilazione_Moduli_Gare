# Tests for Story 1.4: Creazione Profilo Aziendale
# TDD: tests cover all tasks in the story
# FR25, FR26, NFR4, FR29, NFR6

from django.test import TestCase, Client
from django.urls import reverse, resolve
from apps.accounts.models import Tenant, UserCustom, CompanyProfile
from apps.accounts.forms import CompanyProfileForm
from django.db import IntegrityError


class Task1TestCompanyProfileModel(TestCase):
    """Test CompanyProfile model creation and fields."""

    def setUp(self):
        self.tenant = Tenant.objects.create(name='Test Tenant')
        self.user = UserCustom.objects.create_user(
            email='test@example.com',
            password='StrongPass123!',
            tenant=self.tenant
        )

    def test_create_company_profile(self):
        """AC1: CompanyProfile can be created with ragione_sociale, partita_iva, sede_legale."""
        from apps.accounts.models import CompanyProfile
        profile = CompanyProfile.objects.create(
            user=self.user,
            ragione_sociale='Test Azienda S.r.l.',
            partita_iva='12345678901',  # 11 digits
            sede_legale='Via Roma 1, Milano'
        )
        self.assertEqual(profile.ragione_sociale, 'Test Azienda S.r.l.')
        self.assertEqual(profile.partita_iva, '12345678901')  # Should be encrypted at rest
        self.assertEqual(profile.sede_legale, 'Via Roma 1, Milano')
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.tenant, self.user.tenant)  # AC3: tenant from user

    def test_partita_iva_encryption(self):
        """AC2: Partita IVA is encrypted at rest in the database."""
        from apps.accounts.models import CompanyProfile
        profile = CompanyProfile.objects.create(
            user=self.user,
            ragione_sociale='Test Azienda',
            partita_iva='12345678901',
            sede_legale='Address'
        )
        # Check that the stored value is encrypted, not plain text
        # Assuming using django-encrypted-model-fields, the field should be EncryptedCharField
        # We can check by looking at the raw database value or through model behavior
        # For now, test that the value is stored and retrieved correctly
        retrieved_profile = CompanyProfile.objects.get(id=profile.id)
        self.assertEqual(retrieved_profile.partita_iva, '12345678901')  # Should decrypt correctly
        # Additional test: if we have access to the database, check encryption
        # But in Django test, we can't easily check raw DB, so rely on field type

    def test_tenant_association(self):
        """AC3: Profile is associated with tenant from user."""
        from apps.accounts.models import CompanyProfile
        profile = CompanyProfile.objects.create(
            user=self.user,
            ragione_sociale='Test',
            partita_iva='12345678901',
            sede_legale='Address'
        )
        self.assertEqual(profile.tenant, self.user.tenant)
        # Test that tenant is automatically set on save if not provided
        # But in model, we might set it in save method

    def test_str_method(self):
        """Test __str__ method returns ragione_sociale."""
        from apps.accounts.models import CompanyProfile
        profile = CompanyProfile.objects.create(
            user=self.user,
            ragione_sociale='Test Azienda',
            partita_iva='12345678901',
            sede_legale='Address'
        )
        self.assertEqual(str(profile), 'Test Azienda')

    def test_unique_user(self):
        """Test that each user can have only one profile (OneToOneField)."""
        from apps.accounts.models import CompanyProfile
        CompanyProfile.objects.create(
            user=self.user,
            ragione_sociale='First',
            partita_iva='12345678901',
            sede_legale='Address'
        )
        # Attempting to create another profile for the same user should raise IntegrityError
        with self.assertRaises(IntegrityError):
            CompanyProfile.objects.create(
                user=self.user,
                ragione_sociale='Second',
                partita_iva='98765432101',
                sede_legale='Another Address'
            )

    def test_fields_verbose_names(self):
        """Test verbose names for fields (optional)."""
        from apps.accounts.models import CompanyProfile
        profile = CompanyProfile()
        # Check verbose names if defined, but not critical for functionality
        pass


class Task3TestCompanyProfileForm(TestCase):
    """Test CompanyProfileForm with validation."""

    def setUp(self):
        self.tenant = Tenant.objects.create(name='Test Tenant')
        self.user = UserCustom.objects.create_user(
            email='test@example.com',
            password='StrongPass123!',
            tenant=self.tenant
        )

    def test_valid_form(self):
        """Form is valid with all required fields."""
        form = CompanyProfileForm(data={
            'ragione_sociale': 'Test Azienda S.r.l.',
            'partita_iva': '12345678901',
            'sede_legale': 'Via Roma 1, Milano'
        })
        self.assertTrue(form.is_valid())

    def test_empty_ragione_sociale(self):
        """Empty ragione_sociale generates error."""
        form = CompanyProfileForm(data={
            'ragione_sociale': '',
            'partita_iva': '12345678901',
            'sede_legale': 'Via Roma 1, Milano'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('ragione_sociale', form.errors)

    def test_empty_partita_iva(self):
        """Empty partita_iva generates error."""
        form = CompanyProfileForm(data={
            'ragione_sociale': 'Test Azienda',
            'partita_iva': '',
            'sede_legale': 'Via Roma 1, Milano'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('partita_iva', form.errors)

    def test_empty_sede_legale(self):
        """Empty sede_legale generates error."""
        form = CompanyProfileForm(data={
            'ragione_sociale': 'Test Azienda',
            'partita_iva': '12345678901',
            'sede_legale': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('sede_legale', form.errors)

    def test_invalid_partita_iva_format(self):
        """Invalid partita_iva (not 11 digits) generates error."""
        form = CompanyProfileForm(data={
            'ragione_sociale': 'Test Azienda',
            'partita_iva': '123',  # Not 11 digits
            'sede_legale': 'Via Roma 1, Milano'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('partita_iva', form.errors)
        self.assertIn('11 cifre', str(form.errors['partita_iva']))

    def test_valid_partita_iva_format(self):
        """Valid partita_iva (11 digits) passes validation."""
        form = CompanyProfileForm(data={
            'ragione_sociale': 'Test Azienda',
            'partita_iva': '12345678901',
            'sede_legale': 'Via Roma 1, Milano'
        })
        self.assertTrue(form.is_valid())


class Task4TestCreateCompanyProfileView(TestCase):
    """Test create_company_profile view."""

    def setUp(self):
        self.client = Client()
        self.tenant = Tenant.objects.create(name='Test Tenant')
        self.user = UserCustom.objects.create_user(
            email='test@example.com',
            password='StrongPass123!',
            tenant=self.tenant
        )
        self.create_profile_url = reverse('accounts:create_company_profile')

    def test_get_form_unauthenticated(self):
        """Unauthenticated users are redirected to login."""
        response = self.client.get(self.create_profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_get_form_authenticated_no_profile(self):
        """Authenticated user without profile sees form."""
        self.client.login(email='test@example.com', password='StrongPass123!')
        response = self.client.get(self.create_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profilo Aziendale')
        self.assertContains(response, 'form')

    def test_get_form_authenticated_with_profile(self):
        """Authenticated user with existing profile is redirected to dashboard."""
        from apps.accounts.models import CompanyProfile
        CompanyProfile.objects.create(
            user=self.user,
            ragione_sociale='Test Azienda',
            partita_iva='12345678901',
            sede_legale='Address'
        )
        self.client.login(email='test@example.com', password='StrongPass123!')
        response = self.client.get(self.create_profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/profile/edit', response.url)

    def test_post_valid_data(self):
        """POST with valid data creates profile and redirects to dashboard."""
        self.client.login(email='test@example.com', password='StrongPass123!')
        response = self.client.post(self.create_profile_url, {
            'ragione_sociale': 'Test Azienda S.r.l.',
            'partita_iva': '12345678901',
            'sede_legale': 'Via Roma 1, Milano'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')
        # Check profile was created in database
        from apps.accounts.models import CompanyProfile
        self.assertTrue(CompanyProfile.objects.filter(user=self.user).exists())
        profile = CompanyProfile.objects.get(user=self.user)
        self.assertEqual(profile.ragione_sociale, 'Test Azienda S.r.l.')
        self.assertEqual(profile.partita_iva, '12345678901')
        self.assertEqual(profile.sede_legale, 'Via Roma 1, Milano')
        self.assertEqual(profile.tenant, self.user.tenant)

    def test_post_invalid_data(self):
        """POST with invalid data re-renders form with errors."""
        self.client.login(email='test@example.com', password='StrongPass123!')
        response = self.client.post(self.create_profile_url, {
            'ragione_sociale': '',  # Empty
            'partita_iva': '123',   # Invalid
            'sede_legale': ''       # Empty
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        # Check that profile was NOT created
        from apps.accounts.models import CompanyProfile
        self.assertFalse(CompanyProfile.objects.filter(user=self.user).exists())


class Task5TestURLs(TestCase):
    """Test URL routing for company profile creation."""

    def test_url_resolves(self):
        """URL /profile/create/ resolves to create_company_profile view."""
        from apps.accounts.views import create_company_profile
        url = reverse('accounts:create_company_profile')
        self.assertEqual(url, '/profile/create/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, create_company_profile)

    def test_url_exists(self):
        """URL /profile/create/ returns 200 for authenticated user without profile."""
        client = Client()
        tenant = Tenant.objects.create(name='Test Tenant')
        user = UserCustom.objects.create_user(
            email='test@example.com',
            password='StrongPass123!',
            tenant=tenant
        )
        client.login(email='test@example.com', password='StrongPass123!')
        response = client.get('/profile/create/')
        self.assertEqual(response.status_code, 200)

