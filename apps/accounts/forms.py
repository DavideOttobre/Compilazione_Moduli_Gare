# AC-02: Form di Registrazione
# FR30: Autenticazione email/password
# Validazioni: email unica, password robusta, conferma password

from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import UserCustom, Tenant


class RegistrationForm(forms.Form):
    """
    Form di registrazione utente con email e password.

    Satisfies: AC-02 (campi email, password, password_confirm)
    """
    # AC-02: campi email, password, password_confirm
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'inserisci la tua email'
        }),
        error_messages={
            'required': 'L\'email è obbligatoria.',
            'invalid': 'Inserisci un indirizzo email valido.'
        }
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'inserisci la password'
        }),
        validators=[validate_password],
        error_messages={
            'required': 'La password è obbligatoria.'
        }
    )

    password_confirm = forms.CharField(
        label='Conferma Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'conferma la password'
        }),
        error_messages={
            'required': 'La conferma della password è obbligatoria.'
        }
    )

    # AC-02: Validazione email unica
    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if UserCustom.objects.filter(email=email).exists():
            raise forms.ValidationError('Un account con questa email esiste già.')
        return email

    # AC-02: Validazione conferma password
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Le password non corrispondono.')
        return password_confirm
