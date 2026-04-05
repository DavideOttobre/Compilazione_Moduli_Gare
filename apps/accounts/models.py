# AC-01: Custom User Model con Tenant
# FR30: Autenticazione email/password
# FR29: Isolamento dati tra tenant
# NFR7: Autenticazione sicura con hashing

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class Tenant(models.Model):
    """
    Modello Tenant per isolamento dati multi-tenant.

    Satisfies: FR29 (isolamento dati tra tenant), NFR6
    """
    # AC-01: Tenant con id, name, created_at
    name = models.CharField(max_length=255, verbose_name='Nome Azienda')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data Creazione')

    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    """
    Custom Manager per UserCustom.

    Satisfies: AC-01 (create_user, create_superuser)
    """

    # AC-01: Implementare UserManager con create_user() e create_superuser()
    def create_user(self, email, password=None, tenant=None, **extra_fields):
        # AC-01: email obbligatoria
        if not email:
            raise ValueError('L\'email è obbligatoria')

        email = self.normalize_email(email)
        user = self.model(email=email, tenant=tenant, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Il superuser deve avere is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Il superuser deve avere is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class UserCustom(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model esteso con tenant e email come campo di login.

    Satisfies: AC-01 (UserCustom), FR30 (email/password auth)
    """
    # AC-01: UserCustom estende AbstractBaseUser
    email = models.EmailField(unique=True, verbose_name='Email')
    # AC-01: campo tenant ForeignKey
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='Tenant'
    )
    first_name = models.CharField(max_length=150, blank=True, verbose_name='Nome')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Cognome')
    is_active = models.BooleanField(default=True, verbose_name='Attivo')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Data Registrazione')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email

    def get_short_name(self):
        return self.first_name or self.email
