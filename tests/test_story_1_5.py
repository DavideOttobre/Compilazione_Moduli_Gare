# Story 1.5: Test Modifica Profilo Aziendale
# TDD: test prima del codice

from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import Tenant, UserCustom, CompanyProfile


class EditCompanyProfileViewTest(TestCase):
    """
    Test per la view edit_company_profile.
    AC1: Utente con profilo può modificare dati e salvarli
    AC2: Dati aggiornati usati nelle prossime compilazioni
    """

    def setUp(self):
        self.client = Client()
        self.tenant = Tenant.objects.create(name='Test Azienda')
        self.user = UserCustom.objects.create_user(
            email='test@example.com',
            password='TestPassword123!',
            tenant=self.tenant
        )
        self.profile = CompanyProfile.objects.create(
            user=self.user,
            tenant=self.tenant,
            ragione_sociale='Azienda S.r.l.',
            partita_iva='12345678901',
            sede_legale='Via Roma 1, Roma'
        )
        self.edit_url = reverse('accounts:edit_company_profile')

    # --- Test accesso ---

    def test_edit_profile_requires_login(self):
        """AC1: Utente non autenticato non può accedere alla modifica."""
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_edit_profile_requires_existing_profile(self):
        """AC1: Utente senza profilo viene redirect a create."""
        user_no_profile = UserCustom.objects.create_user(
            email='noprofile@example.com',
            password='TestPassword123!',
            tenant=self.tenant
        )
        self.client.login(email='noprofile@example.com', password='TestPassword123!')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('profile/create', response.url)

    def test_edit_profile_get_shows_form(self):
        """AC1: GET mostra form pre-compilato con dati attuali."""
        self.client.login(email='test@example.com', password='TestPassword123!')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')
        self.assertContains(response, 'Azienda S.r.l.')
        self.assertContains(response, '12345678901')
        self.assertContains(response, 'Via Roma 1, Roma')

    # --- Test POST valido ---

    def test_edit_profile_post_valid_data(self):
        """AC1: POST valido aggiorna il profilo."""
        self.client.login(email='test@example.com', password='TestPassword123!')
        response = self.client.post(self.edit_url, {
            'ragione_sociale': 'Nuova Azienda S.p.A.',
            'partita_iva': '98765432101',
            'sede_legale': 'Via Milano 2, Milano'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('dashboard', response.url)
        # Verifica dati salvati
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.ragione_sociale, 'Nuova Azienda S.p.A.')
        self.assertEqual(self.profile.partita_iva, '98765432101')
        self.assertEqual(self.profile.sede_legale, 'Via Milano 2, Milano')

    def test_edit_profile_updated_data_persisted(self):
        """AC2: Dati aggiornati sono effettivamente salvati e recuperabili."""
        self.client.login(email='test@example.com', password='TestPassword123!')
        self.client.post(self.edit_url, {
            'ragione_sociale': 'Azienda Aggiornata',
            'partita_iva': '11111111111',
            'sede_legale': 'Via Nuova 10'
        })
        # Ricarica dal DB e verifica
        profile = CompanyProfile.objects.get(user=self.user)
        self.assertEqual(profile.ragione_sociale, 'Azienda Aggiornata')
        self.assertEqual(profile.partita_iva, '11111111111')
        self.assertEqual(profile.sede_legale, 'Via Nuova 10')

    def test_edit_profile_tenant_unchanged(self):
        """AC2: Il tenant non cambia dopo la modifica."""
        self.client.login(email='test@example.com', password='TestPassword123!')
        self.client.post(self.edit_url, {
            'ragione_sociale': 'Test Tenant',
            'partita_iva': '22222222222',
            'sede_legale': 'Via Test'
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.tenant, self.tenant)

    # --- Test validazione ---

    def test_edit_profile_invalid_partita_iva(self):
        """AC1: P.IVA non valida viene respinta."""
        self.client.login(email='test@example.com', password='TestPassword123!')
        response = self.client.post(self.edit_url, {
            'ragione_sociale': 'Azienda Test',
            'partita_iva': '123',
            'sede_legale': 'Via Test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '11 cifre')

    def test_edit_profile_empty_ragione_sociale(self):
        """AC1: Ragione sociale obbligatoria."""
        self.client.login(email='test@example.com', password='TestPassword123!')
        response = self.client.post(self.edit_url, {
            'ragione_sociale': '',
            'partita_iva': '12345678901',
            'sede_legale': 'Via Test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'obbligatoria')

    def test_edit_profile_empty_sede_legale(self):
        """AC1: Sede legale obbligatoria."""
        self.client.login(email='test@example.com', password='TestPassword123!')
        response = self.client.post(self.edit_url, {
            'ragione_sociale': 'Azienda Test',
            'partita_iva': '12345678901',
            'sede_legale': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'obbligatoria')

    # --- Test isolamento tenant ---

    def test_edit_profile_only_own_profile(self):
        """AC1: Utente modifica solo il proprio profilo."""
        other_tenant = Tenant.objects.create(name='Altro Tenant')
        other_user = UserCustom.objects.create_user(
            email='other@example.com',
            password='TestPassword123!',
            tenant=other_tenant
        )
        CompanyProfile.objects.create(
            user=other_user,
            tenant=other_tenant,
            ragione_sociale='Altra Azienda',
            partita_iva='99999999999',
            sede_legale='Via Altra'
        )
        self.client.login(email='test@example.com', password='TestPassword123!')
        self.client.post(self.edit_url, {
            'ragione_sociale': 'Mia Azienda Modificata',
            'partita_iva': '12345678901',
            'sede_legale': 'Via Roma 1'
        })
        # Verifica che il proprio profilo sia modificato
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.ragione_sociale, 'Mia Azienda Modificata')
        # Verifica che l'altro profilo non sia toccato
        other_profile = CompanyProfile.objects.get(user=other_user)
        self.assertEqual(other_profile.ragione_sociale, 'Altra Azienda')


class CreateProfileRedirectTest(TestCase):
    """
    Test per Task 4: create_company_profile redirect se profilo esiste.
    """

    def setUp(self):
        self.client = Client()
        self.tenant = Tenant.objects.create(name='Test Tenant')
        self.user_with_profile = UserCustom.objects.create_user(
            email='withprofile@example.com',
            password='TestPassword123!',
            tenant=self.tenant
        )
        CompanyProfile.objects.create(
            user=self.user_with_profile,
            tenant=self.tenant,
            ragione_sociale='Azienda Esistente',
            partita_iva='11111111111',
            sede_legale='Via Esistente'
        )
        self.create_url = reverse('accounts:create_company_profile')

    def test_create_redirects_to_edit_if_profile_exists(self):
        """Task 4: Se profilo esiste, create redirect a edit."""
        self.client.login(email='withprofile@example.com', password='TestPassword123!')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('profile/edit', response.url)

    def test_create_shows_form_if_no_profile(self):
        """Task 4: Se profilo non esiste, create mostra form."""
        user_no_profile = UserCustom.objects.create_user(
            email='noprofile@example.com',
            password='TestPassword123!',
            tenant=self.tenant
        )
        self.client.login(email='noprofile@example.com', password='TestPassword123!')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/create_profile.html')
