---
story_id: "1.1"
title: "Setup Django Project"
epic: "1 - Setup & User Management"
status: "ready-for-dev"
assigned_to: ""
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
- [ ] Tutti i task completati
- [ ] Struttura del progetto creata secondo le specifiche
- [ ] Configurazione env funzionante
- [ ] Logging configurato
- [ ] Custom exceptions definite
- [ ] `python manage.py check` passa senza errori
- [ ] Commit effettuato con messaggio appropriato