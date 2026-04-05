---
story_id: "1.1"
title: "Setup Django Project"
epic: "1 - Setup & User Management"
status: "done"
assigned_to: "Amelia"
created_at: "2026-04-05"
updated_at: "2026-04-05"
acceptance_criteria_ref: "epics.md - Story 1.1"
---

# Story 1.1: Setup Django Project

## Contesto
Questa è la prima story del progetto. Creerà la fondazione per tutto lo sviluppo successivo.

## Criteri di Accettazione (da epics.md)
- **Given** the project repository is empty,
- **When** I run the initial setup,
- **Then** the Django project is created with the modular structure: `core/llm/`, `apps/pipeline/`, `apps/document_parser/`, `apps/field_analyzer/`, `apps/questionnaire/`, `apps/compiler/`
- **And** configuration uses environment variables (`variables.env`, `secrets.env`)
- **And** logging is configured with levels DEBUG/INFO/WARNING/ERROR/CRITICAL
- **And** custom exceptions are defined: `DocumentParseError`, `FieldAnalysisError`, `CompilationError`

## Task da completare

### Task 1: Inizializzazione progetto Django
- Creare un nuovo progetto Django nella directory root
- Configurare il file `settings.py` per usare la struttura modulare
- Creare i file `__init__.py` necessari

### Task 2: Struttura modulare delle app
Creare le seguenti directory e file base:
```
core/
  __init__.py
  llm/
    __init__.py
apps/
  __init__.py
  pipeline/
    __init__.py
    models.py
    views.py
  document_parser/
    __init__.py
    models.py
    views.py
  field_analyzer/
    __init__.py
    models.py
    views.py
  questionnaire/
    __init__.py
    models.py
    views.py
  compiler/
    __init__.py
    models.py
    views.py
```

### Task 3: Configurazione con variabili d'ambiente
- Creare i file `variables.env` e `secrets.env` (con esempi)
- Configurare `settings.py` per leggere da questi file (usando python-decouple o django-environ)
- Aggiungere `.env` al `.gitignore`

### Task 4: Configurazione logging
- Configurare Django logging con livelli: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Configurare formatter e handler appropriati
- Includere log di console e file

### Task 5: Custom exceptions
- Creare file `core/exceptions.py`
- Definire le seguenti eccezioni:
  - `DocumentParseError`
  - `FieldAnalysisError`
  - `CompilationError`
- Documentare l'uso previsto per ogni eccezione

### Task 6: Verifica finale
- Eseguire `python manage.py check` per verificare la configurazione
- Creare un test base per verificare che il progetto sia avviabile
- Commit iniziale con struttura del progetto

## Contesto tecnico (da architecture.md)
- **Stack**: Python, Django
- **Database**: SQLite (MVP) → PostgreSQL (produzione)
- **Frontend**: Django Templates con HTMX minimo
- **LLM**: LiteLLM via OpenRouter
- **Document processing**: python-docx, pdfplumber
- **Naming conventions**:
  - Modelli: CamelCase
  - Campi: snake_case
  - Funzioni: snake_case (verbo-sostantivo)
  - Costanti: UPPER_SNAKE_CASE

## Note per lo sviluppatore
- Questa è una story greenfield: inizia da zero
- Seguire le convenzioni definite in architecture.md
- Testare ogni componente prima di procedere
- La struttura deve essere modulare per supportare le pipeline future

## Dipendenze
- Nessuna. Questa è la prima story del progetto.

## Definizione di "Done"
- [x] Tutti i task completati
- [x] Struttura del progetto creata secondo le specifiche
- [x] Configurazione env funzionante
- [x] Logging configurato
- [x] Custom exceptions definite
- [x] `python manage.py check` passa senza errori
- [x] Commit effettuato con messaggio appropriato

---

## Dev Agent Record

### Amelia — Implementation Notes

**Data:** 2026-04-05
**Agent:** Amelia (bmad-dev)

#### Decisioni tecniche
- `python-decouple` scelto su `django-environ` per semplicità API e compatibilità con file `.env` non-standard
- Helper `_get()` implementato per merge prioritizzato secrets.env > variables.env > default
- `AppConfig` esplicito per ogni app (richiesto da Django 6.0.3 con INSTALLED_APPS puntati a sotto-moduli)
- Logging: 2 file handler separati (INFO+ e WARNING+) per separare log operativi da errori
- `AiTenderBaseError` base class aggiunta per catchabilità unificata di tutte le eccezioni custom
- `LANGUAGE_CODE = 'it-it'`, `TIME_ZONE = 'Europe/Rome'` per localizzazione corretta

#### Test creati
- `tests/test_story_1_1.py` — 34 test, 4 classi:
  - `TestModularStructure` (10 test) — AC-01
  - `TestEnvironmentConfiguration` (6 test) — AC-02
  - `TestLoggingConfiguration` (8 test) — AC-03
  - `TestCustomExceptions` (10 test) — AC-04
- Risultato: **34/34 PASSING**

#### AC Traceability
| AC | Codice | Test |
|----|--------|------|
| AC-01 struttura modulare | `INSTALLED_APPS` in `settings.py:79-92`, `apps/*/apps.py`, `core/` | `TestModularStructure` (10 test) |
| AC-02 env vars | `settings.py:22-73` (`_get()`, `RepositoryEnv`) | `TestEnvironmentConfiguration` (6 test) |
| AC-03 logging | `settings.py:168-282` (`LOGGING` dict, `LOG_DIR`) | `TestLoggingConfiguration` (8 test) |
| AC-04 exceptions | `core/exceptions.py` (`DocumentParseError`, `FieldAnalysisError`, `CompilationError`) | `TestCustomExceptions` (10 test) |

### File List
| File | Azione |
|------|--------|
| `manage.py` | Creato (django-admin) |
| `ai_tender/__init__.py` | Creato (django-admin) |
| `ai_tender/settings.py` | Creato + configurato (env vars, logging, INSTALLED_APPS) |
| `ai_tender/urls.py` | Creato (django-admin) |
| `ai_tender/wsgi.py` | Creato (django-admin) |
| `ai_tender/asgi.py` | Creato (django-admin) |
| `core/__init__.py` | Creato |
| `core/llm/__init__.py` | Creato |
| `core/exceptions.py` | Creato (DocumentParseError, FieldAnalysisError, CompilationError) |
| `apps/__init__.py` | Creato |
| `apps/pipeline/__init__.py` | Creato |
| `apps/pipeline/apps.py` | Creato (PipelineConfig) |
| `apps/pipeline/models.py` | Creato (vuoto) |
| `apps/pipeline/views.py` | Creato (vuoto) |
| `apps/document_parser/__init__.py` | Creato |
| `apps/document_parser/apps.py` | Creato (DocumentParserConfig) |
| `apps/document_parser/models.py` | Creato (vuoto) |
| `apps/document_parser/views.py` | Creato (vuoto) |
| `apps/field_analyzer/__init__.py` | Creato |
| `apps/field_analyzer/apps.py` | Creato (FieldAnalyzerConfig) |
| `apps/field_analyzer/models.py` | Creato (vuoto) |
| `apps/field_analyzer/views.py` | Creato (vuoto) |
| `apps/questionnaire/__init__.py` | Creato |
| `apps/questionnaire/apps.py` | Creato (QuestionnaireConfig) |
| `apps/questionnaire/models.py` | Creato (vuoto) |
| `apps/questionnaire/views.py` | Creato (vuoto) |
| `apps/compiler/__init__.py` | Creato |
| `apps/compiler/apps.py` | Creato (CompilerConfig) |
| `apps/compiler/models.py` | Creato (vuoto) |
| `apps/compiler/views.py` | Creato (vuoto) |
| `tests/__init__.py` | Creato |
| `tests/test_story_1_1.py` | Creato (34 test, 4 classi) |
| `static/` | Creato (dir) |
| `templates/` | Creato (dir) |
| `logs/` | Creato auto (settings.py) |
