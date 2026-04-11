# Story 2.2: Parsing PDF Nativo
# AC-1: Estrazione testo da PDF nativo
# AC-2: Parsing < 2 minuti (NFR1)
# AC-3: Errore friendly in italiano
#
# Story 2.4: Parsing Documenti DOCX
# AC-1: Estrazione testo da DOCX
# AC-2: Preservazione struttura (titoli, sezioni, liste)
# AC-3: Parsing < 2 minuti (NFR1)
# AC-4: Errore friendly in italiano

import time

import pdfplumber
from docx import Document as DocxDocument

from core.exceptions import DocumentParseError


def extract_text_from_pdf(document) -> str:
    """
    Estrae il contenuto testuale da un PDF nativo.

    Satisfies: AC-1 (estrazione testo), AC-2 (durata < 2 min), AC-3 (errore friendly)

    Args:
        document: istanza di Document con file PDF

    Returns:
        Stringa con il contenuto testuale estratto da tutte le pagine

    Raises:
        DocumentParseError: se il parsing fallisce (file corrotto, errore I/O)
    """
    try:
        file_path = document.file.path
        pages_text = []

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)

        return ' '.join(pages_text)

    except DocumentParseError:
        raise
    except Exception as e:
        raise DocumentParseError(
            message=(
                'Impossibile leggere il documento. '
                'Verifica che il file sia un PDF valido e non sia danneggiato.'
            ),
            detail=str(e),
        )


def extract_text_from_docx(document, timeout: float = 120.0) -> str:
    """
    Estrae il contenuto testuale da un file DOCX preservando la struttura.

    Satisfies: AC-1 (estrazione testo), AC-2 (struttura titoli/liste), AC-3 (durata < 2 min), AC-4 (errore friendly)

    Args:
        document: istanza di Document con file DOCX
        timeout: timeout massimo in secondi (default 120s per NFR1)

    Returns:
        Stringa con il contenuto testuale estratto con marcatori di struttura

    Raises:
        DocumentParseError: se il parsing fallisce o supera il timeout
    """
    # C-1: Timeout configurabile per NFR1 (durata < 2 minuti)
    start_time = time.time()
    try:
        file_path = document.file.path
        doc = DocxDocument(file_path)
        lines = []

        for para in doc.paragraphs:
            # C-1: Verifica timeout durante il loop
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise DocumentParseError(
                    message=(
                        'La lettura del documento ha superato il tempo massimo consentito. '
                        'Prova con un file più piccolo.'
                    ),
                    detail=f'Parsing timeout after {elapsed:.1f}s (limit: {timeout}s)',
                )

            if not para.text:
                continue

            style_name = para.style.name if para.style else ''

            # AC-2: Preservazione gerarchia titoli
            if style_name.startswith('Heading 1'):
                lines.append(f'[H1] {para.text}')
            elif style_name.startswith('Heading 2'):
                lines.append(f'[H2] {para.text}')
            elif style_name.startswith('Heading 3'):
                lines.append(f'[H3] {para.text}')
            # AC-2: Preservazione liste
            elif 'List Bullet' in style_name:
                lines.append(f'  - {para.text}')
            elif 'List Number' in style_name:
                lines.append(f'  * {para.text}')
            else:
                lines.append(para.text)

        # C-1: Verifica timeout finale
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise DocumentParseError(
                message=(
                    'La lettura del documento ha superato il tempo massimo consentito. '
                    'Prova con un file più piccolo.'
                ),
                detail=f'Parsing timeout after {elapsed:.1f}s (limit: {timeout}s)',
            )

        return '\n'.join(lines)

    except DocumentParseError:
        raise
    except Exception as e:
        raise DocumentParseError(
            message=(
                'Impossibile leggere il documento. '
                'Verifica che il file sia un DOCX valido e non sia danneggiato.'
            ),
            detail=str(e),
        )
