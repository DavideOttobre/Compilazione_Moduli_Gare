# Tests for Story 1.3: Login e Session Management
# TDD: tests cover all tasks in the story
# FR30, NFR7, NFR5

from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from apps.accounts.models import Tenant, UserCustom
from apps.accounts.forms import LoginForm
from apps.accounts.views import LoginView, LogoutView

User = get_user_model()


class Task1TestLoginForm(TestCase):
    """Test LoginForm with email and password fields."""

    def test_valid_form(self):
        """Form is valid with email and password."""
        form = LoginForm(data={
            'email': 'test@example.com',
            'password': 'StrongPass123!'
        })
        self.assertTrue(form.is_valid())

    def test_empty_email(self):
        """Empty email generates error."""
        form = LoginForm(data={
            'email': '',
            'password': 'StrongPass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('obbligatoria', str(form.errors['email']))

    def test_empty_password(self):
        """Empty password generates error."""
        form = LoginForm(data={
            'email': 'test@example.com',
            'password': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertIn('obbligatoria', str(form.errors['password']))

    def test_invalid_email(self):
        """Invalid email format generates error."""
        form = LoginForm(data={
            'email': 'not-an-email',
            'password': 'StrongPass123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class Task1TestLoginView(TestCase):
    """Test LoginView (GET and POST)."""

    def setUp(self):
        self.client = Client()
        self.login_url = '/login/'
        self.tenant = Tenant.objects.create(name='Test Tenant')
        self.user = UserCustom.objects.create_user(
            email='test@example.com',
            password='StrongPass123!',
            tenant=self.tenant
        )

    def test_get_login_view(self):
        """GET /login/ shows login form."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Accedi')
        self.assertContains(response, 'form')

    def test_post_valid_login(self):
        """POST with valid credentials logs in and redirects to dashboard."""
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'StrongPass123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')
        self.assertIn('_auth_user_id', self.client.session)

    def test_post_invalid_credentials(self):
        """POST with wrong password shows error and re-renders form."""
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'WrongPass123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credenziali non valide')

    def test_post_nonexistent_user(self):
        """POST with non-existent email shows error."""
        response = self.client.post(self.login_url, {
            'email': 'nonexistent@example.com',
            'password': 'StrongPass123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credenziali non valide')

    def test_post_inactive_user(self):
        """POST with inactive user shows error."""
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'StrongPass123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credenziali non valide')


class Task2TestLogoutView(TestCase):
    """Test LogoutView."""

    def setUp(self):
        self.client = Client()
        self.logout_url = '/logout/'
        self.tenant = Tenant.objects.create(name='Test Tenant')
        self.user = UserCustom.objects.create_user(
            email='test@example.com',
            password='StrongPass123!',
            tenant=self.tenant
        )
        self.client.login(email='test@example.com', password='StrongPass123!')

    def test_logout_redirects_to_login(self):
        """GET /logout/ invalidates session and redirects to login."""
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_clears_session(self):
        """Logout clears the session."""
        # Verify user is logged in
        self.assertIn('_auth_user_id', self.client.session)
        # Logout
        self.client.get(self.logout_url)
        # Verify user is no longer in session
        self.assertNotIn('_auth_user_id', self.client.session)


class Task3TestSessionTimeout(TestCase):
    """Test session timeout configuration (30 minutes)."""

    def test_session_cookie_age_setting(self):
        """SESSION_COOKIE_AGE is set to 1800 seconds (30 minutes)."""
        from django.conf import settings
        self.assertEqual(settings.SESSION_COOKIE_AGE, 1800)

    def test_session_expire_at_browser_close(self):
        """SESSION_EXPIRE_AT_BROWSER_CLOSE is True."""
        from django.conf import settings
        self.assertTrue(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)

    def test_session_engine_is_db(self):
        """Sessions are stored in database (default)."""
        from django.conf import settings
        self.assertEqual(settings.SESSION_ENGINE, 'django.contrib.sessions.backends.db')


class Task4TestLoginTemplate(TestCase):
    """Test login template content."""

    def setUp(self):
        self.client = Client()
        self.login_url = '/login/'

    def test_template_has_form_fields(self):
        """Login template has email and password fields."""
        response = self.client.get(self.login_url)
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'type="submit"')

    def test_template_has_link_to_register(self):
        """Login template has link to registration page."""
        response = self.client.get(self.login_url)
        self.assertContains(response, 'href="/register/"')

    def test_template_has_error_container(self):
        """Login template has container for error messages."""
        response = self.client.post(self.login_url, {'email': '', 'password': ''})
        self.assertContains(response, 'class="errorlist"')

class Task5TestURLConfiguration(TestCase):
    """Test URL routing for login and logout."""

    def test_login_url_resolves(self):
        """/login/ resolves to LoginView."""
        resolved = resolve('/login/')
        self.assertEqual(resolved.func.view_class.__name__, "LoginView")
        self.assertEqual(resolved.url_name, 'login')

    def test_logout_url_resolves(self):
        """/logout/ resolves to LogoutView."""
        resolved = resolve('/logout/')
        self.assertEqual(resolved.func.view_class.__name__, "LogoutView")
        self.assertEqual(resolved.url_name, 'logout')

    def test_app_name_is_accounts(self):
        """app_name is 'accounts'."""
        resolved = resolve('/login/')
        self.assertEqual(resolved.app_name, 'accounts')


class Task6TestDashboardProtection(TestCase):
    """Test dashboard protection with login_required."""

    def setUp(self):
        self.client = Client()
        self.dashboard_url = '/dashboard/'
        self.login_url = '/login/'
        self.tenant = Tenant.objects.create(name='Test Tenant')
        self.user = UserCustom.objects.create_user(
            email='test@example.com',
            password='StrongPass123!',
            tenant=self.tenant
        )

    def test_unauthenticated_redirects_to_login(self):
        """Unauthenticated user accessing dashboard is redirected to login."""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_authenticated_can_access_dashboard(self):
        """Authenticated user can access dashboard."""
        self.client.login(email='test@example.com', password='StrongPass123!')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')

    def test_next_parameter_preserved(self):
        """Redirect to login preserves 'next' parameter for post-login redirect."""
        response = self.client.get(self.dashboard_url)
        self.assertIn('next=', response.url)


class Task7TestItalianErrorMessages(TestCase):
    """Test that error messages are in Italian."""

    def setUp(self):
        self.client = Client()
        self.login_url = '/login/'

    def test_invalid_credentials_italian(self):
        """Invalid credentials error message is in Italian."""
        response = self.client.post(self.login_url, {
            'email': 'nonexistent@example.com',
            'password': 'WrongPass123!'
        })
        self.assertContains(response, 'Credenziali non valide')

    def test_form_errors_italian(self):
        """Form validation error messages are in Italian."""
        response = self.client.post(self.login_url, {
            'email': '',
            'password': ''
        })
        self.assertContains(response, 'obbligatoria')
