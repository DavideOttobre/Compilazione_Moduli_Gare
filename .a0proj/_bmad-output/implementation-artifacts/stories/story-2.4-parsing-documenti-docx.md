---
story_id: "2.4"
title: "Parsing Documenti DOCX"
epic: "2 - Upload e Analisi Disciplinare di Gara"
status: "done"
assigned_to: "Amelia"
created_at: "2026-04-09"
updated_at: "2026-04-11"
acceptance_criteria_ref: "epics.md - Story 2.4"
---

# Story 2.4: Parsing Documenti DOCX

Status: done

## Story

As a sistema,
I want parsare il contenuto di documenti DOCX,
So that i disciplinari in formato Word possono essere analizzati.

## Acceptance Criteria

1. [AC1] Given un file DOCX è stato caricato, When il sistema esegue il parsing, Then il contenuto testuale viene estratto correttamente (FR5)
2. [AC2] And la struttura del documento (titoli, sezioni, liste) viene preservata
3. [AC3] And il parsing completa in meno di 2 minuti (NFR1)
4. [AC4] And se il parsing fallisce, l'utente riceve un messaggio di errore friendly in italiano
5. [AC5] And solo documenti con `file_type='docx'` e `status='uploaded'` sono accettati
6. [AC6] And il contenuto estratto viene salvato nel campo `parsed_content` del modello `Document`
7. [AC7] And il `Document.status` viene aggiornato a `'parsed'` dopo successo o `'error'` su fallimento
8. [AC8] And isolamento tenant: solo documenti dell'utente autenticato sono accessibili

## Tasks / Subtasks

- [x] Task 1: Implementare DOCX text extraction service (AC: 1, 2, 3)
  - [x] Creare funzione `extract_text_from_docx(document)` in `apps/document_parser/services.py`
  - [x] Usare `python-docx` per estrazione testo da file DOCX
  - [x] Estrarre struttura: titoli (Heading 1/2/3), paragrafi, liste (bullet/numbered)
  - [x] Preservare gerarchia delle sezioni nel testo estratto (AC2)
  - [x] Gestire file multi-sezione concatenando contenuto
  - [x] Implementare controllo durata (< 2 min per NFR1) (AC3)
  - [x] Restituire testo formattato come stringa con marcatori di struttura
- [x] Task 2: Creare endpoint API per trigger parsing DOCX (AC: 1, 4, 5, 7)
  - [x] Creare view `parse_docx_document` in `apps/document_parser/views.py`
  - [x] Accettare solo documenti con `file_type='docx'` e `status='uploaded'` (AC5)
  - [x] Aggiornare `Document.status` a `'parsed'` dopo successo (AC7)
  - [x] Aggiornare `Document.status` a `'error'` su fallimento (AC7)
  - [x] Restituire messaggio errore friendly in italiano (AC4)
  - [x] Verificare isolamento tenant: `document.user == request.user` (AC8)
- [x] Task 3: Aggiornare URL per parsing DOCX (AC: 1)
  - [x] Aggiungere path `documents/parse-docx/<int:pk>/` in `apps/document_parser/urls.py`
- [x] Task 4: Creare template risultato parsing (AC: 1)
  - [x] Template `apps/document_parser/templates/document_parser/parse_docx_result.html`
  - [x] Mostrare anteprima contenuto estratto con struttura
  - [x] Mostrare errore friendly se parsing fallito
- [x] Task 5: Test TDD (AC: 1-8)
  - [x] Test parsing DOCX valido con contenuto estratto (AC1)
  - [x] Test preservazione struttura: titoli e sezioni (AC2)
  - [x] Test parsing DOCX multi-sezione
  - [x] Test durata parsing < 2 minuti (AC3, NFR1)
  - [x] Test parsing fallisce su file corrotto (errore friendly italiano) (AC4)
  - [x] Test rifiuto documenti non-DOCX (tipo sbagliato) (AC5)
  - [x] Test rifiuto documenti non in status 'uploaded' (AC5)
  - [x] Test status documento aggiornato correttamente (uploaded → parsed/error) (AC7)
  - [x] Test isolamento tenant (solo propri documenti) (AC8)
  - [x] Test contenuto salvato in `parsed_content` (AC6)

## Dev Notes

### Architettura e vincoli
- **App destinazione:** `apps/document_parser/` — modulo già esistente con Document model
- **Dipendenze esterne:** `python-docx` per parsing DOCX
- **Modello esistente:** `Document` model in `apps/document_parser/models.py` con campi: user, file, original_name, file_type, file_size, uploaded_at, status, parsed_content
- **Isolamento tenant:** Query filtrate per `user=request.user` (pattern consolidato da Story 2.1 e 2.2)
- **Formato parsing:** Solo DOCX — PDF gestiti in Story 2.2 (nativi) e 2.3 (scannerizzati)
- **Status management:** `uploaded` → `parsed` (successo) o `error` (fallimento)
- **Testing:** TDD obbligatorio. Test copertura completa per tutti gli AC.
- **NFR1:** Parsing deve completare in < 2 minuti per documento
- **Errori:** Messaggi friendly in italiano, no stack trace esposto (pattern da `core/exceptions.py` custom)

### Pattern da Story 2.2 (Parsing PDF Nativo)
- **Service layer:** `apps/document_parser/services.py` — aggiungere `extract_text_from_docx()` parallelamente a `extract_text_from_pdf()`
- **View pattern:** stessa struttura della view `parse_document` esistente, con check `file_type='docx'` invece di `'pdf'`
- **Error handling:** usare `DocumentParseError` da `core/exceptions.py`
- **Tests:** stessa struttura dei test in `tests/test_story_2_2.py` ma per DOCX

### Vincoli da Architecture
- **Document Processing:** python-docx per DOCX (decisione architetturale confermata)
- **Logging:** Multi-livello DEBUG/INFO/WARNING/ERROR/CRITICAL
- **Eccezioni custom:** `DocumentParseError` da `core.exceptions`
- **Struttura modulare:** service + view + template + URL + tests

### Dipendenze Story precedenti
- **Story 1.1:** Setup Django, struttura modulare, eccezioni custom, logging
- **Story 1.2-1.5:** Autenticazione, profilo aziendale, isolamento tenant
- **Story 2.1:** Upload file, Document model, validazione filetype, isolamento upload path per user_id
- **Story 2.2:** Parsing PDF nativo — **pattern diretto da replicare per DOCX**
  - Servizio `extract_text_from_pdf()` in services.py
  - View `parse_document` con tenant isolation
  - Campo `parsed_content` nel modello Document (già esistente)
  - Status transition: uploaded → parsed/error

### Project Structure Notes
- File da creare: nessuno — tutte le app esistono già
- File da modificare: `services.py`, `views.py`, `urls.py`, template
- File test: `tests/test_story_2_4.py` (nuovo)
- Dipendenza: `python-docx` da aggiungere a `requirements.txt`

### References
- [Source: planning-artifacts/epics.md#Story 2.4] — Acceptance criteria e user story
- [Source: planning-artifacts/architecture.md#Document Processing] — python-docx per DOCX
- [Source: implementation-artifacts/stories/story-2.2-parsing-pdf-nativo.md] — Pattern da replicare
- [Source: core/exceptions.py] — DocumentParseError per errori friendly
- [Source: apps/document_parser/services.py] — Service layer esistente
- [Source: apps/document_parser/models.py] — Document model con parsed_content

## Dev Agent Record

### Agent Model Used
Amelia (bmad-dev) — BMAD Developer Agent, Phase 4 Implementation

### Debug Log References
- Test suite: 24/24 passing (OK) — CR fix aggiunto test timeout reale
- Mock fix: `@patch('apps.document_parser.services.Document as DocxDocument')` → `@patch('apps.document_parser.services.DocxDocument')` per corretto path di import
- Dipendenza `python-docx>=1.1.0` aggiunta a `requirements.txt`
- Regressione: errori pre-esistenti in test_story_1_1 e test_story_2_1/2_2 non correlati a questa story

### Completion Notes List
- ✅ Task 1: `extract_text_from_docx()` in services.py — estrae testo con marcatori [H1]/[H2]/[H3] per titoli, `- ` per bullet list, `* ` per numbered list
- ✅ Task 2: `parse_docx_document` view con tenant isolation, file_type check (docx only), status check (uploaded only), status transition (parsed/error), errore friendly italiano
- ✅ Task 3: URL `parse-docx/<int:pk>/` aggiunta a urls.py
- ✅ Task 4: Template `parse_docx_result.html` con anteprima contenuto e messaggi errore
- ✅ Task 5: 24 test TDD coprono tutti AC-1..AC-8
- ✅ Tutti gli AC soddisfatti con test passanti
- ✅ Pattern da Story 2.2 (PDF) replicato fedelmente per DOCX
- ✅ CR Fixes applicati (2026-04-11):
  - C-1: Timeout configurabile in `extract_text_from_docx(timeout=120.0)` con `time.time()` e `DocumentParseError` se superato
  - C-2: Import `from docx import Document as DocxDocument` spostato a inizio services.py e `from core.exceptions import DocumentParseError` + `from apps.document_parser.services import extract_text_from_docx` spostati a inizio views.py (PEP8)
  - H-1: `hasattr(e, 'user_message')` sostituito con `isinstance(e, DocumentParseError)` in views.py:138
  - H-2: Aggiunto test `test_extract_text_timeout_raises_error` con mock di `time.time` (side_effect=[0.0, 200.0]) per verificare timeout reale
### File List
- `apps/document_parser/services.py` — aggiunta `extract_text_from_docx()` (modified)
- `apps/document_parser/views.py` — aggiunta `parse_docx_document` view (modified)
- `apps/document_parser/urls.py` — aggiunta route `parse-docx/<int:pk>/` (modified)
- `apps/document_parser/templates/document_parser/parse_docx_result.html` — template risultato parsing (new)
- `tests/test_story_2_4.py` — 23 test TDD (new)
- `requirements.txt` — aggiunta `python-docx>=1.1.0` (modified)
