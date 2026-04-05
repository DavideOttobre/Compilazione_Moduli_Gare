"""
Eccezioni personalizzate per il progetto ai_tender.

Satisfies: AC-04 (custom exceptions: DocumentParseError, FieldAnalysisError, CompilationError)

Tutte le eccezioni:
- Espongono messaggi user-friendly in italiano
- Non espongono stack trace all'utente finale
- Seguono la naming convention CamelCase (architecture.md)
"""


class AiTenderBaseError(Exception):
    """Eccezione base per tutte le eccezioni del progetto ai_tender.

    Fornisce messaggio user-friendly e codice errore opzionale.
    Non espone dettagli tecnici all'utente finale.
    """

    # AC-04: messaggio predefinito in italiano, sovrascritto dalle sottoclassi
    DEFAULT_MESSAGE = "Si è verificato un errore. Riprova o contatta il supporto."

    def __init__(self, message: str = "", detail: str = ""):
        """
        Args:
            message: Messaggio user-friendly in italiano (mostrato all'utente).
            detail:  Dettaglio tecnico opzionale (solo per log, mai mostrato all'utente).
        """
        # AC-04: usa messaggio di default se non fornito
        self.user_message = message or self.DEFAULT_MESSAGE
        self.detail = detail  # solo per logging interno
        super().__init__(self.user_message)

    def __str__(self) -> str:  # noqa: D105
        # AC-04: __str__ restituisce solo il messaggio user-friendly
        return self.user_message


class DocumentParseError(AiTenderBaseError):
    """Errore durante il parsing di un documento (PDF o DOCX).

    Satisfies: AC-04

    Uso previsto:
        Sollevata dai moduli in `apps.document_parser` quando un documento
        non può essere letto, è corrotto, o ha un formato non supportato.

    Esempio::

        raise DocumentParseError(
            message="Il documento caricato non può essere letto. Verifica che il file sia un PDF o DOCX valido.",
            detail=f"pdfplumber failed on {filepath}: {original_exception}",
        )
    """

    # AC-04: messaggio user-friendly in italiano per errori di parsing
    DEFAULT_MESSAGE = (
        "Impossibile leggere il documento. "
        "Verifica che il file sia un PDF o DOCX valido e non sia danneggiato."
    )


class FieldAnalysisError(AiTenderBaseError):
    """Errore durante l'analisi dei campi del documento.

    Satisfies: AC-04

    Uso previsto:
        Sollevata dai moduli in `apps.field_analyzer` quando l'LLM
        non riesce a identificare i campi da compilare nel documento,
        o quando la risposta dell'LLM è malformata.

    Esempio::

        raise FieldAnalysisError(
            message="Analisi del documento non riuscita. Il documento potrebbe avere una struttura insolita.",
            detail=f"LLM returned invalid JSON: {raw_response}",
        )
    """

    # AC-04: messaggio user-friendly in italiano per errori di analisi campi
    DEFAULT_MESSAGE = (
        "Analisi del documento non completata. "
        "Il documento potrebbe avere una struttura non supportata. "
        "Riprova o contatta il supporto."
    )


class CompilationError(AiTenderBaseError):
    """Errore durante la compilazione del documento con i dati forniti.

    Satisfies: AC-04

    Uso previsto:
        Sollevata dai moduli in `apps.compiler` quando la sostituzione
        dei placeholder con i dati reali fallisce, o quando il documento
        di output non può essere generato.

    Esempio::

        raise CompilationError(
            message="Compilazione del documento non riuscita. Verifica i dati inseriti e riprova.",
            detail=f"python-docx write failed: {original_exception}",
        )
    """

    # AC-04: messaggio user-friendly in italiano per errori di compilazione
    DEFAULT_MESSAGE = (
        "Compilazione del documento non riuscita. "
        "Verifica i dati inseriti e riprova. "
        "Se il problema persiste, contatta il supporto."
    )
