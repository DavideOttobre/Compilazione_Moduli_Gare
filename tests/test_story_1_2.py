# AC-06: Test completa per Story 1.2 — Registrazione Utente con Email
# TDD: test coprono tutti i task della story
# FR30, FR29, NFR7

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from apps.accounts.models import Tenant, UserCustom, UserManager
from apps.accounts.forms import RegistrationForm
from apps.accounts.views import RegisterView, DashboardView
from apps.accounts.managers import TenantAwareManager, TenantManagerMixin

User = get_user_model()


class Task1TestTenantModel(TestCase):
    """AC-01: Test modello Tenant."""

    def test_tenant_creation(self):
        """AC-01: Tenant può essere creato con name."""
        tenant = Tenant.objects.create(name='Edilizia Rossi S.r.l.')
        self.assertIsNotNone(tenant.id)
        self.assertEqual(tenant.name, 'Edilizia Rossi S.r.l.')
        self.assertIsNotNone(tenant.created_at)

    def test_tenant_str(self):
        """AC-01: __str__ restituisce il nome."""
        tenant = Tenant.objects.create(name='Test S.p.A.')
        self.assertEqual(str(tenant), 'Test S.p.A.')

    def test_tenant_ordering(self):
        """AC-01: Tenant ordinati per created_at desc."""
        t1 = Tenant.objects.create(name='Primo')
        t2 = Tenant.objects.create(name='Secondo')
        tenants = list(Tenant.objects.values_list('name', flat=True))
        self.assertEqual(tenants[0], 'Secondo')
        self.assertEqual(tenants[1], 'Primo')


class Task1TestUserCustomModel(TestCase):
    """AC-01: Test modello UserCustom esteso AbstractBaseUser."""

    def setUp(self):
        self.tenant = Tenant.objects.create(name='Test Tenant')

    def test_user_creation_with_tenant(self):
        """AC-01: UserCustom creato con tenant associato."""
        user = UserCustom.objects.create_user(
            email='test@example.com',
            password='StrongPass123!',
            tenant=self.tenant
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.tenant, self.tenant)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_user_str(self):
        """AC-01: __str__ restituisce email."""
        user = UserCustom.objects.create_user(
            email='str@example.com', password='StrongPass123!', tenant=self.tenant
        )
        self.assertEqual(str(user), 'str@example.com')

    def test_user_username_field_is_email(self):
        """FR30: USERNAME_FIELD è email."""
        self.assertEqual(UserCustom.USERNAME_FIELD, 'email')

    def test_user_required_fields(self):
        """AC-01: REQUIRED_FIELDS è vuoto (email basta)."""
        self.assertEqual(UserCustom.REQUIRED_FIELDS, [])

    def test_get_full_name(self):
        """AC-01: get_full_name() restituisce nome completo."""
        user = UserCustom.objects.create_user(
            email='full@example.com', password='StrongPass123!',
            tenant=self.tenant, first_name='Mario', last_name='Rossi'
        )
        self.assertEqual(user.get_full_name(), 'Mario Rossi')

    def test_get_full_name_fallback(self):
        """AC-01: get_full_name() fallback a email se nome vuoto."""
        user = UserCustom.objects.create_user(
            email='nofull@example.com', password='StrongPass123!', tenant=self.tenant
        )
        self.assertEqual(user.get_full_name(), 'nofull@example.com')

    def test_get_short_name(self):
        """AC-01: get_short_name() restituisce first_name."""
        user = UserCustom.objects.create_user(
            email='short@example.com', password='StrongPass123!',
            tenant=self.tenant, first_name='Mario'
        )
        self.assertEqual(user.get_short_name(), 'Mario')

    def test_user_without_tenant(self):
        """AC-01: UserCustom può esistere senza tenant (null=True)."""
        user = UserCustom.objects.create_user(
            email='notenant@example.com', password='StrongPass123!'
        )
        self.assertIsNone(user.tenant)


class Task1TestUserManager(TestCase):
    """AC-01: Test UserManager con create_user/create_superuser."""

    def setUp(self):
        self.tenant = Tenant.objects.create(name='Manager Test')

    def test_create_user(self):
        """AC-01: create_user() crea utente con password hashata."""
        user = UserCustom.objects.create_user(
            email='user@example.com',
            password='StrongPass123!',
            tenant=self.tenant
        )
        self.assertTrue(user.check_password('StrongPass123!'))
        self.assertNotEqual(user.password, 'StrongPass123!')

    def test_create_user_no_email_raises(self):
        """AC-01: create_user() senza email solleva ValueError."""
        with self.assertRaises(ValueError):
            UserCustom.objects.create_user(email='', password='StrongPass123!')

    def test_create_superuser(self):
        """AC-01: create_superuser() crea utente con is_staff e is_superuser."""
        admin = UserCustom.objects.create_superuser(
            email='admin@example.com', password='StrongPass123!'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_superuser_no_staff_raises(self):
        """AC-01: create_superuser() con is_staff=False solleva ValueError."""
        with self.assertRaises(ValueError):
            UserCustom.objects.create_superuser(
                email='bad@example.com', password='StrongPass123!', is_staff=False
            )

    def test_create_superuser_no_superuser_raises(self):
        """AC-01: create_superuser() con is_superuser=False solleva ValueError."""
        with self.assertRaises(ValueError):
            UserCustom.objects.create_superuser(
                email='bad2@example.com', password='StrongPass123!', is_superuser=False
            )


class Task2TestAuthConfig(TestCase):
    """AC-02: Test configurazione backend auth."""

    def test_auth_user_model_configured(self):
        """AC-02: AUTH_USER_MODEL punta a accounts.UserCustom."""
        from django.conf import settings
        self.assertEqual(settings.AUTH_USER_MODEL, 'accounts.UserCustom')

    def test_accounts_in_installed_apps(self):
        """AC-02: apps.accounts è in INSTALLED_APPS."""
        from django.conf import settings
        self.assertIn('apps.accounts', settings.INSTALLED_APPS)

    def test_password_hashing(self):
        """NFR7: Password hashata con PBKDF2 (Django default, NFR7 compliant)."""
        user = UserCustom.objects.create_user(
            email='hash@example.com', password='StrongPass123!'
        )
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))
        self.assertNotEqual(user.password, 'StrongPass123!')
        self.assertTrue(user.check_password('StrongPass123!'))
        self.assertFalse(user.check_password('WrongPass'))


class Task3TestRegistrationForm(TestCase):
    """AC-03: Test form di registrazione con validazioni."""

    def test_valid_form(self):
        """AC-03: Form valido con email e password corrette."""
        form = RegistrationForm(data={
            'email': 'valid@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """AC-03: Email non valida genera errore."""
        form = RegistrationForm(data={
            'email': 'not-an-email',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_empty_email(self):
        """AC-03: Email vuota genera errore."""
        form = RegistrationForm(data={
            'email': '',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_duplicate_email(self):
        """AC-03: Email già registrata genera errore."""
        UserCustom.objects.create_user(email='taken@example.com', password='StrongPass123!')
        form = RegistrationForm(data={
            'email': 'taken@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('già', str(form.errors['email']))

    def test_password_mismatch(self):
        """AC-03: Password diverse genera errore."""
        form = RegistrationForm(data={
            'email': 'mismatch@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'DifferentPass456!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password_confirm', form.errors)
        self.assertIn('non corrispondono', str(form.errors['password_confirm']))

    def test_weak_password(self):
        """AC-03: Password troppo debole genera errore (Django validators)."""
        form = RegistrationForm(data={
            'email': 'weak@example.com',
            'password': '123',
            'password_confirm': '123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_empty_password(self):
        """AC-03: Password vuota genera errore."""
        form = RegistrationForm(data={
            'email': 'nopass@example.com',
            'password': '',
            'password_confirm': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_empty_password_confirm(self):
        """AC-03: Conferma password vuota genera errore."""
        form = RegistrationForm(data={
            'email': 'noconf@example.com',
            'password': 'StrongPass123!',
            'password_confirm': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password_confirm', form.errors)


class Task4TestRegisterView(TestCase):
    """AC-04: Test view di registrazione (GET/POST)."""

    def setUp(self):
        self.client = Client()
        self.register_url = '/register/'

    def test_get_register_view(self):
        """AC-04: GET /register/ mostra form."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertContains(response, 'Registrati')

    def test_post_valid_registration(self):
        """AC-04: POST valido crea tenant + user + login automatico."""
        response = self.client.post(self.register_url, {
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        })
        # AC-04: redirect a dashboard dopo registrazione
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')
        # Verifica utente creato
        self.assertTrue(UserCustom.objects.filter(email='newuser@example.com').exists())
        # Verifica tenant creato
        user = UserCustom.objects.get(email='newuser@example.com')
        self.assertIsNotNone(user.tenant)
        self.assertEqual(user.tenant.name, 'Azienda di newuser@example.com')
        # Verifica login automatico
        self.assertIn('_auth_user_id', self.client.session)

    def test_post_invalid_form_shows_errors(self):
        """AC-04: POST non valido mostra errori."""
        response = self.client.post(self.register_url, {
            'email': '',
            'password': '',
            'password_confirm': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'email', status_code=200)

    def test_post_duplicate_email_shows_error(self):
        """AC-04: Email duplicata mostra errore."""
        UserCustom.objects.create_user(email='exists@example.com', password='StrongPass123!')
        response = self.client.post(self.register_url, {
            'email': 'exists@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'già')


class Task6TestURLRouting(TestCase):
    """AC-05: Test URL configuration."""

    def test_register_url_resolves(self):
        """AC-05: /register/ risolve a RegisterView."""
        resolved = resolve('/register/')
        self.assertEqual(resolved.func.view_class.__name__, "RegisterView")
        self.assertEqual(resolved.url_name, 'register')

    def test_dashboard_url_resolves(self):
        """AC-05: /dashboard/ risolve a DashboardView."""
        resolved = resolve('/dashboard/')
        self.assertEqual(resolved.func.view_class.__name__, "DashboardView")
        self.assertEqual(resolved.url_name, 'dashboard')

    def test_app_name_is_accounts(self):
        """AC-05: app_name è 'accounts'."""
        resolved = resolve('/register/')
        self.assertEqual(resolved.app_name, 'accounts')


class Task7TestTenantIsolation(TestCase):
    """AC-06: Test isolamento tenant (FR29 — zero cross-tenant leakage)."""

    def setUp(self):
        self.tenant1 = Tenant.objects.create(name='Tenant Alpha')
        self.tenant2 = Tenant.objects.create(name='Tenant Beta')
        self.user1 = UserCustom.objects.create_user(
            email='alpha@example.com', password='StrongPass123!', tenant=self.tenant1
        )
        self.user2 = UserCustom.objects.create_user(
            email='beta@example.com', password='StrongPass123!', tenant=self.tenant2
        )

    def test_tenant_manager_mixin_exists(self):
        """AC-06: TenantManagerMixin ha for_tenant()."""
        self.assertTrue(hasattr(TenantManagerMixin, 'for_tenant'))

    def test_tenant_aware_manager_exists(self):
        """AC-06: TenantAwareManager è un Manager."""
        from django.db import models
        self.assertTrue(issubclass(TenantAwareManager, models.Manager))
        self.assertTrue(issubclass(TenantAwareManager, TenantManagerMixin))

    def test_tenant_isolation_users(self):
        """FR29: Utenti del tenant1 non sono visibili dal tenant2."""
        users_tenant1 = UserCustom.objects.filter(tenant=self.tenant1)
        users_tenant2 = UserCustom.objects.filter(tenant=self.tenant2)
        self.assertIn(self.user1, users_tenant1)
        self.assertNotIn(self.user1, users_tenant2)
        self.assertIn(self.user2, users_tenant2)
        self.assertNotIn(self.user2, users_tenant1)

    def test_tenant_cascade_delete(self):
        """AC-06: Eliminare tenant elimina utenti associati (CASCADE)."""
        tenant_id = self.tenant1.id
        user_id = self.user1.id
        self.tenant1.delete()
        self.assertFalse(UserCustom.objects.filter(id=user_id).exists())
        self.assertFalse(Tenant.objects.filter(id=tenant_id).exists())

    def test_users_have_separate_tenants(self):
        """FR29: Due utenti hanno tenant separati."""
        self.assertNotEqual(self.user1.tenant, self.user2.tenant)
        self.assertEqual(self.user1.tenant.name, 'Tenant Alpha')
        self.assertEqual(self.user2.tenant.name, 'Tenant Beta')


class Task8TestPasswordHashing(TestCase):
    """NFR7: Test hashing password bcrypt/PBKDF2."""

    def test_password_is_hashed(self):
        """NFR7: Password non è salvata in chiaro."""
        user = UserCustom.objects.create_user(
            email='hash2@example.com', password='MySecretPass123!'
        )
        self.assertNotEqual(user.password, 'MySecretPass123!')
        self.assertIn('$', user.password)  # hash separator

    def test_pbkdf2_hasher_used(self):
        """NFR7: PBKDF2 è il hasher di default (Django default, NFR7 compliant)."""
        user = UserCustom.objects.create_user(
            email='pbkdf2@example.com', password='StrongPass123!'
        )
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))

    def test_check_password_works(self):
        """NFR7: check_password() funziona con hash."""
        user = UserCustom.objects.create_user(
            email='check@example.com', password='CorrectPass123!'
        )
        self.assertTrue(user.check_password('CorrectPass123!'))
        self.assertFalse(user.check_password('WrongPass123!'))

    def test_set_password_hashes(self):
        """NFR7: set_password() applica hash."""
        user = UserCustom()
        user.set_password('NewPass123!')
        self.assertNotEqual(user.password, 'NewPass123!')
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))
        self.assertTrue(user.check_password('NewPass123!'))
