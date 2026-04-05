# AC-03: View di Registrazione
# FR30: Autenticazione email/password
# NFR7: Session timeout 30 minuti

import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View

from .forms import RegistrationForm, LoginForm
from .models import Tenant, UserCustom

logger = logging.getLogger('apps.accounts')


class RegisterView(View):
    """
    View per la registrazione utente.
    GET: mostra form di registrazione
    POST: valida form, crea tenant + user, login automatico

    Satisfies: AC-03 (GET/POST), AC-04 (login automatico), FR30
    """
    template_name = 'accounts/register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                tenant = Tenant.objects.create(name=f'Azienda di {email}')
                logger.info(f'Tenant creato: {tenant.name} (id={tenant.id})')

                user = UserCustom.objects.create_user(
                    email=email,
                    password=password,
                    tenant=tenant
                )
                logger.info(f'Utente registrato: {email} (tenant={tenant.name})')

                login(request, user)

                messages.success(request, f'Registrazione completata con successo! Benvenuto, {email}.')
                return redirect('accounts:dashboard')

            except Exception as e:
                logger.error(f'Errore registrazione: {e}')
                messages.error(request, 'Si è verificato un errore durante la registrazione. Riprova.')
                return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """
    View per il login utente.
    GET: mostra form di login
    POST: autentica e crea sessione

    Satisfies: FR30 (login email/password), Task 1 Story 1.3
    """
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email'].lower().strip()
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info(f'Login effettuato: {email}')
                    messages.success(request, f'Benvenuto, {email}!')
                    next_url = request.GET.get('next', 'accounts:dashboard')
                    return redirect(next_url)
                else:
                    logger.warning(f'Tentativo login account disattivato: {email}')
                    messages.error(request, 'Credenziali non valide.')
            else:
                logger.warning(f'Tentativo login fallito: {email}')
                messages.error(request, 'Credenziali non valide.')

        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """
    View per il logout utente.
    Invalida la sessione corrente e redirect a login.

    Satisfies: Task 2 Story 1.3
    """

    def get(self, request):
        if request.user.is_authenticated:
            email = request.user.email
            logout(request)
            logger.info(f'Logout effettuato: {email}')
            messages.success(request, 'Disconnessione effettuata con successo.')
        return redirect('accounts:login')


class DashboardView(LoginRequiredMixin, View):
    """
    Dashboard per utenti autenticati.
    Richiede login (LoginRequiredMixin).

    Satisfies: Task 6 Story 1.3 (protezione dashboard)
    """
    template_name = 'accounts/dashboard.html'
    login_url = '/login/'  # URL per redirect se non autenticato

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})
