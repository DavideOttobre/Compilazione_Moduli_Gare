# AC-03: View di Registrazione
# FR30: Autenticazione email/password
# NFR7: Session timeout 30 minuti

import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import View

from .forms import RegistrationForm
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

    # AC-03: GET mostra form di registrazione
    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    # AC-03: POST valida form, crea tenant + user, login automatico
    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # AC-03: crea tenant associato all'utente
                tenant = Tenant.objects.create(name=f'Azienda di {email}')
                logger.info(f'Tenant creato: {tenant.name} (id={tenant.id})')

                # AC-03: crea utente con tenant associato
                user = UserCustom.objects.create_user(
                    email=email,
                    password=password,
                    tenant=tenant
                )
                logger.info(f'Utente registrato: {email} (tenant={tenant.name})')

                # AC-04: login automatico dopo registrazione
                login(request, user)

                # AC-04: conferma registrazione e redirect a dashboard
                messages.success(request, f'Registrazione completata con successo! Benvenuto, {email}.')
                return redirect('accounts:dashboard')

            except Exception as e:
                # AC-03: gestione errori con messaggi friendly in italiano
                logger.error(f'Errore registrazione: {e}')
                messages.error(request, 'Si è verificato un errore durante la registrazione. Riprova.')
                return render(request, self.template_name, {'form': form})

        # AC-03: form non valido — mostra errori
        return render(request, self.template_name, {'form': form})


class DashboardView(View):
    """
    Dashboard placeholder post-registrazione.
    """
    template_name = 'accounts/dashboard.html'

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})
