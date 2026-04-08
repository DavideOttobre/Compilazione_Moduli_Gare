# AC-03: View di Registrazione
# FR30: Autenticazione email/password
# NFR7: Session timeout 30 minuti

import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View

from .forms import RegistrationForm, LoginForm, CompanyProfileForm
from .models import Tenant, UserCustom, CompanyProfile

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


@login_required(login_url='/login/')
def create_company_profile(request):
    """
    View per la creazione del profilo aziendale.
    GET: mostra form vuoto (se utente autenticato e senza profilo)
    POST: valida form e crea profilo

    Satisfies: AC-1 (creazione profilo), Task 4 Story 1.4
    """
    # AC-1: e senza profilo esistente
    # AC-1: redirect a edit se profilo esiste
    if hasattr(request.user, 'company_profile'):
        messages.info(request, 'Profilo aziendale già esistente.')
        return redirect('accounts:edit_company_profile')
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST)
        if form.is_valid():
            # AC-1: salva profilo
            profile = form.save(commit=False)
            profile.user = request.user
            # AC-3: tenant from user
            profile.tenant = request.user.tenant
            profile.save()
            logger.info(f'Profilo aziendale creato per {request.user.email}')
            messages.success(request, 'Profilo aziendale creato con successo!')
            return redirect('accounts:dashboard')
    else:
        form = CompanyProfileForm()

    return render(request, 'accounts/create_profile.html', {'form': form})


@login_required(login_url='/login/')
def edit_company_profile(request):
    """
    View per la modifica del profilo aziendale.
    GET: mostra form pre-compilato con dati attuali
    POST: valida form e aggiorna profilo

    Satisfies: AC-1 (modifica profilo), AC-2 (dati aggiornati), Task 1 Story 1.5
    """
    # AC-1: accesso solo utenti con profilo esistente
    try:
        profile = CompanyProfile.objects.get(user=request.user)
    except CompanyProfile.DoesNotExist:
        messages.info(request, 'Crea prima il tuo profilo aziendale.')
        return redirect('accounts:create_company_profile')

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # AC-1: salva modifiche
            form.save()
            logger.info(f'Profilo aziendale aggiornato per {request.user.email}')
            messages.success(request, 'Profilo aziendale aggiornato con successo!')
            return redirect('accounts:dashboard')
    else:
        form = CompanyProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})
