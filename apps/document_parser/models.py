# Story 2.1: Upload File PDF e DOCX
# AC-1: Documento associato a tenant utente
# AC-2: Conferma caricamento con nome file e dimensione
# AC-3: Validazione formato solo PDF/DOCX

from django.db import models
from django.conf import settings


class Document(models.Model):
    """
    Modello per tracciare i documenti caricati dall'utente.

    Satisfies: AC-1 (upload associato a tenant), AC-2 (nome file e dimensione), AC-3 (formato PDF/DOCX)
    """
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
    ]

    STATUS_CHOICES = [
        ('uploaded', 'Caricato'),
        ('parsed', 'Analizzato'),
        ('error', 'Errore'),
    ]

    # AC-1: ForeignKey a User per isolamento tenant
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Utente'
    )
    # AC-1: FileField con upload_to documents/
    file = models.FileField(upload_to='documents/', verbose_name='File')
    # AC-2: Nome originale del file
    original_name = models.CharField(max_length=255, verbose_name='Nome Originale')
    # AC-1/AC-3: Tipo file (pdf o docx)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, verbose_name='Tipo File')
    # AC-2: Dimensione in bytes
    file_size = models.IntegerField(verbose_name='Dimensione (bytes)')
    # Auto timestamp upload
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Data Upload')
    # Stato elaborazione
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='uploaded',
        verbose_name='Stato'
    )

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documenti'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.original_name} ({self.file_type})'

    # Story 2.2: Parsing PDF Nativo - AC-1
    parsed_content = models.TextField(
        blank=True, null=True, verbose_name='Contenuto Estratto'
    )
