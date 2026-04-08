# Story 2.2: Parsing PDF Nativo
# AC-1: Estrazione testo da PDF nativo
# AC-2: Parsing < 2 minuti (NFR1)
# AC-3: Errore friendly in italiano

import pdfplumber

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
