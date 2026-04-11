---
story_id: "2.1"
title: "Upload File PDF e DOCX"
epic: "2 - Upload e Analisi Disciplinare di Gara"
status: "done"
assigned_to: "Amelia"
created_at: "2026-04-08"
updated_at: "2026-04-09"
acceptance_criteria_ref: "epics.md - Story 2.1"
---

# Story 2.1: Upload File PDF e DOCX

Status: done

## Story

As a responsabile amministrativo,
I want caricare un file PDF o DOCX (il disciplinare di gara),
So that il sistema può analizzarlo per identificare i documenti richiesti.

## Acceptance Criteria

1. [AC1] Given l'utente è autenticato e ha un profilo aziendale, When seleziona e carica un file PDF o DOCX, Then il file viene salvato nel sistema associato al tenant dell'utente (FR1, FR2)
2. [AC2] And il sistema conferma il caricamento con nome file e dimensione
3. [AC3] And il formato del file viene validato (solo PDF o DOCX accettati)

## Tasks / Subtasks

- [x] Task 1: Creare model Documento nel modulo document_parser (AC: 1, 2, 3)
  - [x] Creare `Document` model in `apps/document_parser/models.py` con campi:
    - `user` (ForeignKey a User, per isolamento tenant)
    - `file` (FileField con upload_to='documents/')
    - `original_name` (CharField per nome originale)
    - `file_type` (CharField: 'pdf' o 'docx')
    - `file_size` (IntegerField per dimensione in bytes)
    - `uploaded_at` (DateTimeField auto_now_add)
    - `status` (CharField: 'uploaded', 'parsed', 'error')
  - [x] Creare e applicare migration
- [x] Task 2: Creare form per upload documento (AC: 1, 3)
  - [x] Creare `DocumentUploadForm` in `apps/document_parser/forms.py`
  - [x] Validare che il file sia PDF o DOCX (tramite estensione e content_type)
  - [x] Messaggio errore friendly in italiano per formato non valido
- [x] Task 3: Creare view per upload documento (AC: 1, 2, 3)
  - [x] Creare `upload_document` view in `apps/document_parser/views.py` che:
    - Limiti accesso a utenti autenticati con profilo aziendale
    - Gestisca GET (mostra form) e POST (salva documento)
    - Salvi file associato al tenant dell'utente
    - Reindirizza a pagina conferma con nome file e dimensione
    - Gestisca errori di validazione formato
- [x] Task 4: Creare template per upload documento (AC: 1, 2)
  - [x] Creare `apps/document_parser/templates/document_parser/upload.html` con form Bootstrap
  - [x] Creare template conferma upload con nome file e dimensione
- [x] Task 5: Configurare URL routing per upload (AC: 1)
  - [x] Aggiungere URL config in `apps/document_parser/urls.py`
  - [x] Includere URL in `ai_tender/urls.py`
  - [x] Path: `documents/upload/`
- [x] Task 6: Test TDD (AC: 1, 2, 3)
  - [x] Test upload documento PDF valido
  - [x] Test upload documento DOCX valido
  - [x] Test formato non valido (es. .txt, .exe)
  - [x] Test accesso negato per utenti non autenticati
  - [x] Test accesso negato per utenti senza profilo aziendale
  - [x] Test salvataggio corretto nome file, dimensione e tipo
  - [x] Test isolamento tenant (documenti associati a utente corretto)

## Dev Notes

### Architettura e vincoli
- **App destinazione:** `apps/document_parser/` — modulo dedicato al parsing documenti
- **Modello:** Nuovo model `Document` per tracciare i file caricati
- **Isolamento tenant:** Ogni documento è associato all'utente proprietario. Query filtrate per `user=request.user`.
- **Formati accettati:** Solo PDF e DOCX. Validazione su estensione e content_type.
- **Storage:** File salvati in `MEDIA_ROOT/documents/<user_id>/` (o configurazione Django standard)
- **Testing:** TDD obbligatorio. Test completi per upload, validazione, isolamento.
- **Dipendenze:** L'utente deve avere un profilo aziendale (dalla Story 1.4). Verificare con `CompanyProfile.objects.filter(user=request.user).exists()`

### Riferimenti
- [Source: planning-artifacts/epics.md#Story 2.1: Upload File PDF e DOCX]
- [Source: planning-artifacts/architecture.md#Django App Structure]
- [Source: planning-artifacts/prd.md#FR1, FR2]
- [Source: apps/accounts/views.py] (pattern @login_required)
- [Source: apps/accounts/models.py] (modello CompanyProfile per verifica profilo)

### Contexto da Epic 1
- **Autenticazione:** `@login_required` decorator già usato nelle view di accounts
- **Profilo aziendale:** `CompanyProfile` model in `apps/accounts/models.py` — verificare esistenza prima di upload
- **Pattern URL:** Namespace `document_parser` con paths come `documents/upload/`
- **Template base:** `templates/base.html` con Bootstrap per layout consistente
- **Cifratura:** Non necessaria per il file, ma i dati estratti successivamente potranno richiederla

### Struttura implementazione
1. **Model Document:** traccia metadata file (nome, tipo, dimensione, stato)
2. **Form:** validazione formato PDF/DOCX con messaggi errore in italiano
3. **View:** upload con check profilo esistente, salvataggio file, redirect conferma
4. **Template:** form upload Bootstrap + pagina conferma
5. **URL:** `/documents/upload/` nel namespace `document_parser`
6. **Test:** copertura completa per tutti gli AC

## Dev Agent Record

### Agent Model Used

Amelia (bmad-dev) — BMAD Phase 4 Implementation

### Debug Log References

### Completion Notes List

- **Task 1 (Model Document):** Creato model `Document` con tutti i campi richiesti. Migration `0001_initial.py` generata e applicata. 9 test unitari coprono tutti i campi, il default status='uploaded' e il metodo `__str__`.
- **Task 2 (Form):** Implementato `DocumentUploadForm` con validazione estensione e content_type. Messaggi errore in italiano. 5 test coprono accettazione PDF/DOCX e rifiuto TXT/EXE.
- **Task 3-5 (View, URL, Template):** View `upload_document` con decoratore `@login_required` e controllo profilo aziendale. GET mostra form, POST salva documento e redirect a conferma. Template `upload.html` (form Bootstrap) e `upload_success.html` (conferma con nome file e dimensione). URL `documents/upload/` e `documents/upload/success/<pk>/` nel namespace `document_parser`. Incluso in `ai_tender/urls.py`. 8 test coprono tutti i flussi: autenticazione, profilo, upload valido/invalido, conferma, isolamento tenant.
- **Task 6 (Test):** Suite completa di 22 test tutti passanti: 9 model, 5 form, 8 view. Copertura totale degli AC.
- **Admin:** Registrato `Document` in `admin.py` per pannello admin.

### CR Fixes (2026-04-09)

Code review avversariale ha identificato 5 issue (3 HIGH, 2 MEDIUM). Tutte risolte:

- **CR Issue #1 (HIGH):** Aggiunta validazione dimensione massima file (50MB) in `DocumentUploadForm.clean_file()`
- **CR Issue #2 (HIGH):** Fix bug logico content_type — check ora obbligatorio (`if not content_type or ...`)
- **CR Issue #3 (HIGH):** Aggiunta validazione magic bytes (`%PDF` per PDF, `PK\x03\x04` per DOCX)
- **CR Issue #4 (MEDIUM):** Rimosso scope creep Story 2.2 da views.py e urls.py (rimosso `parse_document` view e URL `parse/<int:pk>/`)
- **CR Issue #5 (MEDIUM):** FileField `upload_to` ora usa `user_documents_path` per isolamento fisico per user_id
- Aggiornato `file_size` da `IntegerField` a `PositiveIntegerField`
- Generata migration `0003_cr_fixes_story_2_1.py`
- Aggiunti 11 nuovi test di sicurezza (SecurityValidationTests)
- Suite finale: 33/33 test passanti

### File List

- `apps/document_parser/models.py` — Model Document (CR fix: upload_to user_id, PositiveIntegerField)
- `apps/document_parser/forms.py` — DocumentUploadForm (CR fix: file_size, content_type, magic bytes)
- `apps/document_parser/views.py` — upload_document + upload_success views (CR fix: removed Story 2.2 scope creep)
- `apps/document_parser/urls.py` — URL routing (CR fix: removed parse/ URL)
- `apps/document_parser/admin.py` — Admin registration per Document
- `apps/document_parser/templates/document_parser/upload.html` — Template upload form
- `apps/document_parser/templates/document_parser/upload_success.html` — Template conferma upload
- `apps/document_parser/migrations/0001_initial.py` — Migration iniziale
- `apps/document_parser/migrations/0003_cr_fixes_story_2_1.py` — Migration CR fixes
- `ai_tender/urls.py` — Include document_parser URLs
- `tests/test_story_2_1.py` — 33 test TDD per upload documento (CR fix: +11 security tests)
- `.a0proj/_bmad-output/implementation-artifacts/sprint-status.yaml` — Aggiornato status a 'done'
- `.a0proj/_bmad-output/test-artifacts/review-story-2.1.md` — CR report
