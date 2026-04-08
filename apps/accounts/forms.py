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


class LoginForm(forms.Form):
    """
    Form di login con email e password.

    Satisfies: FR30 (autenticazione email/password), Task 1 Story 1.3
    """
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
        error_messages={
            'required': 'La password è obbligatoria.'
        }
    )


class CompanyProfileForm(forms.ModelForm):
    """
    Form per la creazione del profilo aziendale.

    Satisfies: AC-1 (creazione profilo), AC-2 (validazione P.IVA)
    FR25, FR26
    """
    # AC-1: fields for ragione_sociale, partita_iva, sede_legale
    class Meta:
        from .models import CompanyProfile
        model = CompanyProfile
        fields = ['ragione_sociale', 'partita_iva', 'sede_legale']
        widgets = {
            'ragione_sociale': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'es. Azienda S.r.l.'
            }),
            'partita_iva': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678901 (11 cifre)'
            }),
            'sede_legale': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Via Roma 1, 00100 Roma (RM)'
            }),
        }
        error_messages = {
            'ragione_sociale': {
                'required': 'La ragione sociale è obbligatoria.',
            },
            'partita_iva': {
                'required': 'La partita IVA è obbligatoria.',
            },
            'sede_legale': {
                'required': 'La sede legale è obbligatoria.',
            },
        }

    # AC-2: validazione formato Partita IVA (11 cifre)
    def clean_partita_iva(self):
        partita_iva = self.cleaned_data.get('partita_iva', '').strip()
        if not partita_iva.isdigit() or len(partita_iva) != 11:
            raise forms.ValidationError('La partita IVA deve essere composta da 11 cifre numeriche.')
        return partita_iva
