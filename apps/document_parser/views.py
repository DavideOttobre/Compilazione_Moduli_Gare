# Story 2.1: Upload File PDF e DOCX
# AC-1: Upload documento PDF/DOCX associato a tenant utente
# AC-2: Conferma caricamento con nome file e dimensione
# AC-3: Validazione formato solo PDF/DOCX

import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.accounts.models import CompanyProfile
from apps.document_parser.forms import DocumentUploadForm
from apps.document_parser.models import Document


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


# Story 2.2: Parsing PDF Nativo
# AC-1: Estrazione testo da PDF nativo
# AC-2: Parsing < 2 minuti (NFR1)
# AC-3: Errore friendly in italiano su fallimento

from django.http import HttpResponseBadRequest
from core.exceptions import DocumentParseError
from apps.document_parser.services import extract_text_from_pdf


@login_required(login_url='/login/')
def parse_document(request, pk):
    """
    Trigger parsing PDF per documento.

    Satisfies: AC-1 (estrazione testo), AC-3 (errore friendly)
    Solo per documenti PDF con status='uploaded'.
    """
    try:
        doc = Document.objects.get(pk=pk, user=request.user)
    except Document.DoesNotExist:
        messages.error(request, 'Documento non trovato.')
        return redirect('document_parser:upload_document')

    # AC-1: Solo documenti PDF
    if doc.file_type != 'pdf':
        return HttpResponseBadRequest(
            'Il parsing PDF è disponibile solo per documenti in formato PDF.'
        )

    # AC-1: Solo documenti con status 'uploaded'
    if doc.status != 'uploaded':
        return HttpResponseBadRequest(
            'Questo documento è già stato analizzato o è in errore.'
        )

    context = {
        'document': doc,
        'success': False,
        'error_message': None,
        'parsed_content': None,
    }

    try:
        # AC-1: Estrai testo dal PDF
        content = extract_text_from_pdf(doc)

        # AC-1: Salva contenuto e aggiorna status
        doc.parsed_content = content
        doc.status = 'parsed'
        doc.save()

        context['success'] = True
        context['parsed_content'] = content

    except DocumentParseError as e:
        # AC-3: Errore friendly in italiano
        doc.status = 'error'
        doc.save()
        context['error_message'] = str(e)

    return render(request, 'document_parser/parse_result.html', context)
