# Story 2.1: Upload File PDF e DOCX
# AC-1: Upload documento associato a tenant utente
# AC-3: Validazione formato solo PDF/DOCX
# CR Fixes: file_size validation, content_type bypass, magic bytes

from django import forms


class DocumentUploadForm(forms.Form):
    """
    Form per upload documento PDF o DOCX.

    Satisfies: AC-1 (upload), AC-3 (validazione formato PDF/DOCX)
    """
    # AC-3: Set di estensioni accettate
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    ALLOWED_CONTENT_TYPES = {
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    }
    # Magic bytes per validazione firma file
    MAGIC_BYTES = {
        'pdf': b'%PDF',
        'docx': b'PK\x03\x04',  # DOCX è un ZIP
    }
    # Dimensione massima file: 50MB
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB in bytes

    file = forms.FileField(
        label='Documento di Gara',
        help_text='Formati accettati: PDF, DOCX (max 50MB)',
        error_messages={
            'required': 'Seleziona un file da caricare.',
            'missing': 'Seleziona un file da caricare.',
            'empty': 'Il file selezionato è vuoto.',
            'invalid': 'File non valido.',
        }
    )

    # AC-3: Validazione estensione, content_type, magic bytes e dimensione
    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file is None:
            raise forms.ValidationError('Seleziona un file da caricare.')

        # AC-3: Estrai estensione
        filename = uploaded_file.name
        extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

        # AC-3: Verifica estensione
        if extension not in self.ALLOWED_EXTENSIONS:
            raise forms.ValidationError(
                'Formato non valido. Sono accettati solo file PDF e DOCX.'
            )

        # FIX (CR Issue #2): Verifica content_type — OBBLIGATORIO, non opzionale
        content_type = getattr(uploaded_file, 'content_type', '')
        if not content_type or content_type not in self.ALLOWED_CONTENT_TYPES:
            raise forms.ValidationError(
                'Formato non valido. Sono accettati solo file PDF e DOCX.'
            )

        # FIX (CR Issue #1): Verifica dimensione massima file
        if uploaded_file.size > self.MAX_FILE_SIZE:
            max_mb = self.MAX_FILE_SIZE // (1024 * 1024)
            raise forms.ValidationError(
                f'Il file è troppo grande. Dimensione massima consentita: {max_mb}MB.'
            )

        # Verifica che il file non sia vuoto
        if uploaded_file.size == 0:
            raise forms.ValidationError(
                'Il file selezionato è vuoto.'
            )

        # FIX (CR Issue #3): Verifica magic bytes — firma reale del file
        uploaded_file.seek(0)
        file_header = uploaded_file.read(8)
        uploaded_file.seek(0)

        expected_magic = self.MAGIC_BYTES.get(extension)
        if expected_magic and not file_header.startswith(expected_magic):
            raise forms.ValidationError(
                'Il file non sembra essere un documento valido. '
                'Verifica che il formato del file corrisponda alla sua estensione.'
            )

        return uploaded_file
