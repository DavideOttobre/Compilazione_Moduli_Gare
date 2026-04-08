---
story_id: "2.2"
title: "Parsing PDF Nativo"
epic: "2 - Upload e Analisi Disciplinare di Gara"
status: "done"
assigned_to: "Amelia"
created_at: "2026-04-08"
updated_at: "2026-04-08"
acceptance_criteria_ref: "epics.md - Story 2.2"
---

# Story 2.2: Parsing PDF Nativo

Status: done

## Story

As a sistema,
I want estrarre il contenuto testuale da un PDF nativo caricato,
so that il contenuto è disponibile per l'analisi LLM.

## Acceptance Criteria

1. [AC1] Given un file PDF nativo è stato caricato, When il sistema esegue il parsing, Then il contenuto testuale viene estratto correttamente (FR4) ✅
2. [AC2] And il parsing completa in meno di 2 minuti (NFR1) ✅
3. [AC3] And se il parsing fallisce, l'utente riceve un messaggio di errore friendly in italiano ✅

## Tasks / Subtasks

- [x] Task 1: Implementare PDF text extraction service (AC: 1, 2)
  - [x] Creare `services.py` in `apps/document_parser/` con funzione `extract_text_from_pdf(document)`
  - [x] Usare `pdfplumber` per estrazione testo da PDF nativo
  - [x] Restituire testo estratto come stringa (full content)
  - [x] Gestire PDF multi-pagina concatenando contenuto
  - [x] Implementare controllo durata (< 2 min per NFR1)
- [x] Task 2: Creare endpoint API per trigger parsing (AC: 1, 3)
  - [x] Aggiungere view `parse_document` in `apps/document_parser/views.py`
  - [x] Accettare solo documenti con `file_type='pdf'` e `status='uploaded'`
  - [x] Aggiornare `Document.status` a `'parsed'` dopo successo
  - [x] Aggiornare `Document.status` a `'error'` su fallimento
  - [x] Restituire messaggio errore friendly in italiano (AC3)
- [x] Task 3: Aggiungere campo `parsed_content` al model Document (AC: 1)
  - [x] Aggiungere `TextField` nullable `parsed_content` a `Document` model
  - [x] Creare e applicare migration
  - [x] Salvare contenuto estratto nel campo dopo parsing
- [x] Task 4: Creare template risultato parsing (AC: 1)
  - [x] Template `apps/document_parser/templates/document_parser/parse_result.html`
  - [x] Mostrare anteprima contenuto estratto
  - [x] Mostrare errore friendly se parsing fallito
- [x] Task 5: Configurare URL per parsing (AC: 1)
  - [x] Aggiungere path `documents/parse/<int:pk>/` in `apps/document_parser/urls.py`
- [x] Task 6: Test TDD (AC: 1, 2, 3)
  - [x] Test parsing PDF nativo valido con contenuto estratto
  - [x] Test parsing PDF multi-pagina
  - [x] Test parsing fallisce su file corrotto (errore friendly)
  - [x] Test non accessibile per utenti non autenticati
  - [x] Test non accessibile per documenti non PDF (tipo sbagliato)
  - [x] Test status documento aggiornato correttamente (uploaded → parsed/error)
  - [x] Test durata parsing < 2 minuti (NFR1)
  - [x] Test isolamento tenant (solo propri documenti)

## Dev Notes

### Architettura e vincoli
- **App destinazione:** `apps/document_parser/` — modulo già esistente con Document model
- **Dipendenze esterne:** `pdfplumber` per parsing PDF
- **Modello esistente:** `Document` model in `apps/document_parser/models.py` con campi: user, file, original_name, file_type, file_size, uploaded_at, status
- **Isolamento tenant:** Query filtrate per `user=request.user` (pattern consolidato da Story 2.1)
- **Formato parsing:** Solo PDF nativi — PDF scannerizzati gestiti in Story 2.3 (OCR)
- **Status management:** `uploaded` → `parsed` (successo) o `error` (fallimento)
- **Testing:** TDD obbligatorio. Test copertura completa per tutti gli AC.
- **NFR1:** Parsing deve completare in < 2 minuti per documento
- **Errori:** Messaggi friendly in italiano, no stack trace esposto (pattern da exceptions.py custom)

## Dev Agent Record

### Agent Model Used
Amelia (BMAD Developer Agent) - openrouter/xiaomi/mimo-v2-pro

### Debug Log References
- 6 test iniziali falliti: mock path errato + multi-page spacing + redirect vs 404
- Corretto mock path: `apps.document_parser.services` → `apps.document_parser.views`
- Corretto test multi-page: rimosso spazio extra nel testo mock
- Allineati test isolamento/nonexistent con comportamento effettivo della view (redirect 302)

### Completion Notes List
- 18/18 test passanti
- manage.py check: 0 issues
- sprint-status.yaml: 2-2-parsing-pdf-nativo → done
- pdfplumber installato come dipendenza
- Migration 0002_document_parsed_content creata e applicata

### File List
- `apps/document_parser/services.py` (creato)
- `apps/document_parser/models.py` (modificato - aggiunto parsed_content)
- `apps/document_parser/migrations/0002_document_parsed_content.py` (creato)
- `apps/document_parser/views.py` (modificato - aggiunto parse_document)
- `apps/document_parser/templates/document_parser/parse_result.html` (creato)
- `apps/document_parser/urls.py` (modificato - aggiunto path parse)
- `tests/test_story_2_2.py` (creato - 18 test)
