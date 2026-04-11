# Story 2.1: Upload File PDF e DOCX
# AC-1: Upload documento PDF/DOCX associato a tenant utente
# AC-2: Conferma caricamento con nome file e dimensione
# AC-3: Validazione formato solo PDF/DOCX
# CR Fix #4: Removed Story 2.2 scope creep (parse_document view)

import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.accounts.models import CompanyProfile
from apps.document_parser.forms import DocumentUploadForm
from apps.document_parser.models import Document
from apps.document_parser.services import extract_text_from_docx
from core.exceptions import DocumentParseError


# AC-1: View per upload documento
@login_required(login_url='/login/')
def upload_document(request):
    # AC-1: Verifica profilo aziendale esistente
    has_profile = CompanyProfile.objects.filter(user=request.user).exists()
    if not has_profile:
        messages.error(request, 'Devi prima creare un profilo aziendale per caricare documenti.')
        return redirect('accounts:create_company_profile')

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']

            # AC-1: Estrai metadati file
            original_name = uploaded_file.name
            filename = original_name
            extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
            file_size = uploaded_file.size

            # AC-1: Salva documento associato all'utente
            doc = Document(
                user=request.user,
                file=uploaded_file,
                original_name=original_name,
                file_type=extension,
                file_size=file_size,
            )
            doc.save()

            # AC-2: Redirect a pagina conferma con nome e dimensione
            return redirect('document_parser:upload_success', pk=doc.pk)
    else:
        form = DocumentUploadForm()

    return render(request, 'document_parser/upload.html', {'form': form})


# AC-2: Pagina conferma upload
@login_required(login_url='/login/')
def upload_success(request, pk):
    try:
        doc = Document.objects.get(pk=pk, user=request.user)
    except Document.DoesNotExist:
        messages.error(request, 'Documento non trovato.')
        return redirect('document_parser:upload_document')

    # AC-2: Mostra nome file e dimensione
    context = {
        'document': doc,
        'file_name': doc.original_name,
        'file_size': doc.file_size,
        'file_type': doc.get_file_type_display(),
    }
    return render(request, 'document_parser/upload_success.html', context)


# Story 2.4: Parsing Documenti DOCX
# AC-1: Estrazione testo da DOCX
# AC-4: Errore friendly in italiano
# AC-5: Solo file_type='docx' e status='uploaded'
# AC-7: Status aggiornato a 'parsed' o 'error'
# AC-8: Isolamento tenant


@login_required(login_url='/login/')
def parse_docx_document(request, pk):
    """
    Parsing DOCX: estrae contenuto testuale dal documento DOCX.

    Satisfies: AC-1 (parsing), AC-5 (check filetype/status), AC-7 (status update), AC-8 (tenant isolation)
    """
    # AC-8: Isolamento tenant — solo documenti dell'utente autenticato
    try:
        doc = Document.objects.get(pk=pk, user=request.user)
    except Document.DoesNotExist:
        messages.error(request, 'Documento non trovato.')
        return redirect('document_parser:upload_document')

    # AC-5: Accettare solo file_type='docx'
    if doc.file_type != 'docx':
        messages.error(request, 'Questo endpoint supporta solo documenti DOCX.')
        return render(request, 'document_parser/parse_docx_result.html', {
            'document': doc,
            'success': False,
            'error_message': 'Questo endpoint supporta solo documenti DOCX.',
        }, status=400)

    # AC-5: Accettare solo status='uploaded'
    if doc.status != 'uploaded':
        messages.error(request, 'Questo documento è già stato analizzato.')
        return render(request, 'document_parser/parse_docx_result.html', {
            'document': doc,
            'success': False,
            'error_message': 'Questo documento è già stato analizzato.',
        }, status=400)

    # AC-1: Esegui parsing DOCX
    try:
        parsed_text = extract_text_from_docx(doc)
        # AC-7: Aggiorna status a 'parsed' e salva contenuto (AC-6)
        doc.status = 'parsed'
        doc.parsed_content = parsed_text
        doc.save()

        return render(request, 'document_parser/parse_docx_result.html', {
            'document': doc,
            'success': True,
            'parsed_content': parsed_text,
        })

    except Exception as e:
        # AC-7: Aggiorna status a 'error' su fallimento
        doc.status = 'error'
        doc.save()

        # AC-4: Messaggio errore friendly in italiano
        # H-1: isinstance invece di hasattr
        if isinstance(e, DocumentParseError):
            error_msg = e.user_message
        else:
            error_msg = (
                'Impossibile leggere il documento. '
                'Verifica che il file sia un DOCX valido e non sia danneggiato.'
            )

        return render(request, 'document_parser/parse_docx_result.html', {
            'document': doc,
            'success': False,
            'error_message': error_msg,
        })
