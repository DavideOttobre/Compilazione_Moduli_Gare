# Story 2.1: Upload File PDF e DOCX
# AC-1: Upload documento associato a tenant utente
# AC-3: Validazione formato solo PDF/DOCX

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

    file = forms.FileField(
        label='Documento di Gara',
        help_text='Formati accettati: PDF, DOCX',
        error_messages={
            'required': 'Seleziona un file da caricare.',
            'missing': 'Seleziona un file da caricare.',
            'empty': 'Il file selezionato è vuoto.',
            'invalid': 'File non valido.',
        }
    )

    # AC-3: Validazione estensione e content_type
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

        # AC-3: Verifica content_type
        content_type = getattr(uploaded_file, 'content_type', '')
        if content_type and content_type not in self.ALLOWED_CONTENT_TYPES:
            raise forms.ValidationError(
                'Formato non valido. Sono accettati solo file PDF e DOCX.'
            )

        return uploaded_file
