---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - prd.md
  - product-brief-ai_tender-2026-04-03.md
workflowType: 'architecture'
project_name: 'ai_tender'
user_name: 'Davide'
date: '2026-04-05'
---

# Architecture Decision Document - ai_tender

_Documento che si costruisce collaborativamente passo dopo passo attraverso decisioni architetturali._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
La pipeline agentica deve:
- Analizzare il disciplinare di gara (PDF/Word) per identificare moduli compilabili
- Identificare i campi da compilare nei moduli (spazi vuoti, checkbox)
- Inserire placeholder strutturati nei campi identificati (es. {ragione_sociale}, {piva})
- Generare un questionario dinamico per raccogliere dati variabili specifici della gara
- Compilare automaticamente i documenti sostituendo i placeholder con dati azienda + risposte questionario
- Produrre output finale con layout e formato corretti (Word/PDF)

**Non-Functional Requirements:**
- Velocità: documento compilato in < 5 minuti (vs giorni/settimane con consulente)
- Correttezza: 100% campi compilati correttamente, zero errori formali
- Autonomia: utente completa l'intero processo senza assistenza esterna
- Formato: output finale con layout e contenuto conformi all'originale
- SaaS B2B multi-tenant con isolamento dati tra clienti

**Scale & Complexity:**
- Primary domain: Full-stack SaaS + AI/Automation
- Complexity level: Medium-High
- Estimated architectural components: 7 (Frontend, Backend API, Document Parser/Analyzer, Placeholder Engine, Questionnaire Generator, Document Compiler, Storage/DB)

### Technical Constraints & Dependencies

- Input: documenti Word/PDF di formato variabile (nessuno standard comune tra stazioni appaltanti)
- LLM per analisi documentale complessa (vision + NLP)
- Preservazione layout originale nel documento compilato
- Compliance GDPR per dati azienda sensibili
- Mercato PMI edili — UX semplice, zero learning curve

### Cross-Cutting Concerns Identified

- **Gestione errori robusta**: fallback quando parsing fallisce o campi ambigui
- **Audit trail**: tracciabilità delle decisioni di compilazione
- **Template management**: gestione modelli documenti per diversi bandi
- **Security**: protezione dati azienda, crittografia storage
- **Observability**: logging, monitoring, alerting per pipeline

## Starter Template Decision

### Technical Preferences
- **Backend**: Python + Django
- **Frontend**: Django Templates + HTMX (minimo, non prioritario)
- **LLM**: LiteLLm (multi-provider: OpenAI, Anthropic)
- **Document Processing**: python-docx + pdfplumber
- **Database**: SQLite (MVP) → PostgreSQL (produzione)
- **Dati azienda**: JSON mock (company_data.json) → DB futuro
- **Priority**: Pipeline end-to-end funzionante senza errori

### Architettura Pipeline Core

```
[Upload DOCX/PDF]
       ↓
[1. Document Parser]  → Estrai testo + struttura
       ↓
[2. Field Analyzer]   → LLM identifica campi compilabili
       ↓
[3. Placeholder Engine] → Inserisce {placeholder} nel DOCX
       ↓
[4. Questionnaire]    → Form dinamico per campi non profilo
       ↓
[5. Compiler]         → Sostituisce placeholder con dati mock + risposte
       ↓
[Download DOCX compilato]
```

### Struttura Moduli Django

| App | Responsabilità |
|-----|----------------|
| `pipeline` | Orchestrazione flusso completo, tracking stato |
| `document_parser` | Estrazione testo + struttura da DOCX/PDF |
| `field_analyzer` | Analisi LLM per identificare campi compilabili |
| `placeholder_engine` | Inserimento placeholder strutturati nel documento |
| `questionnaire` | Generazione form dinamico, gestione risposte |
| `compiler` | Caricamento dati mock JSON, sostituzione placeholder |
| `accounts` | Futuro: multi-tenant, profili azienda |

### Strategia "Zero Errori"
- Test unitari per ogni modulo
- Test end-to-end con DOCX reali
- Logging dettagliato ad ogni step
- Fallback graceful: campi non riconosciuti → review manuale
- Validazione output: verifica sostituzione completa placeholder

## Core Architectural Decisions

### Category 1: Architettura Dati
**Decisione**: Modello Semplice (MVP)
**Rationale**: Minima complessità, JSON field per stato pipeline, facilità transizione a DB normalizzato in futuro.
**Dettaglio**:
- Modello `ProcessingJob` con JSON field per tracking stato pipeline completo
- Dati azienda da `company_data.json` (mock) → sostituibile con tabella DB futuro
- Django migrations per evoluzione schema
- Validazione tramite Django built-in validators
- Nessuna cache iniziale (MVP)

### Category 2: Autenticazione & Sicurezza
**Decisione**: Opzione A — Minima (MVP)
**Rationale**: Focus totale sulla pipeline core. Django Admin auth per accesso sviluppo/testing. Multi-tenant e login utenti si aggiungono quando il core funziona.
**Dettaglio**:
- Django built-in auth (Admin)
- Nessun multi-tenant in MVP
- Nessun login utenti frontend
- Security middleware Django default
- CSRF protection attiva

### Category 3: API & Communication
**Decisione**: Opzione A — Django Views classiche
**Rationale**: Frontend minimo, interazione semplice (upload → wait → download). Zero overhead API, paradigma classico Django. DRF futuro se serve frontend ricco o integrazioni esterne.
**Dettaglio**:
- Form POST per upload documento
- Processing sincrono (o async con polling se necessario)
- Redirect o response per download risultato
- Nessuna API REST per ora
- CSRF protection nativa Django

### Category 4: Frontend Architecture
**Decisione**: Django Templates minimo
**Rationale**: Frontend non prioritario. Templates per upload/download. HTMX solo se necessario per polling stato. Nessun framework JS.
**Dettaglio**:
- Django Templates nativi
- Bootstrap o CSS base per styling
- HTMX solo per aggiornamenti parziali (opzionale)
- Nessun React/Vue/Angular
- Interazione: upload form → processing → download link

### Category 5: Infrastructure & Deployment
**Decisione**: Opzione A — Locale
**Rationale**: Evitare complessità infrastrutturale. Focus su testing e pipeline funzionante. Deploy futuro quando MVP validato.
**Dettaglio**:
- Esecuzione locale su macchina sviluppo
- SQLite come database
- Nessun Docker/PaaS in MVP
- Testing locale end-to-end
- Deploy post-MVP quando pipeline validata

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:** 5 aree dove agenti AI potrebbero fare scelte diverse

### Naming Patterns

**Database (Django):**
- Model class: CamelCase → `ProcessingJob`, `QuestionnaireResponse`
- Campi colonne: snake_case → `document_file`, `pipeline_status`
- Foreign key: `{model}_id` → `company_id`
- Index: `idx_{model}_{field}` → `idx_job_status`

**Funzioni Python:**
- snake_case, verbo + sostantivo → `parse_document()`, `extract_fields()`, `compile_output()`

**Variabili:**
- snake_case minuscolo → `company_data`, `pipeline_status`
- Costanti: UPPER_SNAKE_CASE → `MAX_RETRIES`, `DEFAULT_TIMEOUT`

**Template Django:**
- snake_case, prefisso app → `pipeline/upload.html`, `compiler/result.html`

**URL patterns:**
- kebab-case per path → `path('upload-document/', ...)`, `path('pipeline-status/<int:job_id>/', ...)`

### Structure Patterns

**Project Organization:**
```
ai_tender/
├── apps/
│   ├── [app_name]/          # Ogni app Django = modulo pipeline
│   │   ├── models.py        # Modelli specifici
│   │   ├── views.py         # Views classiche
│   │   ├── urls.py          # URL patterns app
│   │   ├── services.py      # Logica business (LLM, processing)
│   │   ├── utils.py         # Helper specifici
│   │   ├── tests/
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   └── test_services.py
│   │   ├── templates/[app_name]/
│   │   └── static/[app_name]/
├── core/                    # Utilities condivise
│   ├── llm/                 # Client LiteLLm unificato
│   ├── documents/           # Parser DOCX/PDF comuni
│   ├── exceptions.py        # Eccezioni custom
│   ├── validators.py        # Validatori comuni
│   └── logging.py           # Configurazione logging
├── templates/               # Template base (layout)
├── static/                  # Static files globali
└── data/
    └── company_data.json    # Dati mock azienda
```

**Test Location:** sottocartella `tests/` in ogni app Django
**Shared utilities:** cartella `core/` alla root del progetto
**Config files:** nella root o in `config/`

### Format Patterns

**Pipeline State JSON (dentro ProcessingJob):**
```json
{
  "status": "processing|completed|failed",
  "steps": {
    "document_parsed": true,
    "fields_analyzed": true,
    "placeholders_inserted": false,
    "questionnaire_generated": false,
    "compiled": false
  },
  "errors": [],
  "metadata": {
    "input_file": "disciplinare_gara.docx",
    "processing_start": "ISO-8601",
    "last_updated": "ISO-8601"
  }
}
```

**Company Data JSON (mock):**
```json
{
  "ragione_sociale": "...",
  "piva": "...",
  "indirizzo": { "via": "...", "cap": "...", "citta": "...", "provincia": "..." },
  "contatti": { "telefono": "...", "email": "...", "pec": "..." }
}
```

### Communication Patterns

**Gestione Errori:**
- Livelli log: DEBUG / INFO / WARNING / ERROR / CRITICAL (standard Python logging)
- Eccezioni custom: `DocumentParseError`, `FieldAnalysisError`, `CompilationError`
- Messaggi utente: friendly, in italiano, senza stack trace
- Fallback: campi non riconosciuti → marcati per review manuale

**Stati Processing:**
- Sincrono per MVP (processing inline, risultato immediato)
- Feedback utente: spinner durante processing
- Se necessario: HTMX polling a `/pipeline/status/<job_id>/`

### Enforcement Guidelines

**Tutti gli agenti DEVONO:**
- ✅ Seguire naming conventions definite sopra
- ✅ Usare struttura project definita (ogni app Django = un modulo)
- ✅ Implementare test per ogni funzione/service
- ✅ Usare client LLM unificato in `core/llm/`
- ✅ Logging stratturato secondo livelli definiti
- ✅ Gestire errori con eccezioni custom + messaggi utente friendly

**Pattern Enforcement:**
- Checklist pre-commit per naming e struttura
- Test unitari + end-to-end obbligatori
- Code review per ogni PR

## Project Structure & Boundaries

### Mapping Requisiti → Moduli

| Requisito Funzionale | Modulo Django | Directory |
|---------------------|---------------|-----------|
| Upload documento | `pipeline` | `apps/pipeline/` |
| Estrazione testo + struttura | `document_parser` | `apps/document_parser/` |
| Analisi LLM campi compilabili | `field_analyzer` | `apps/field_analyzer/` |
| Inserimento placeholder | `placeholder_engine` | `apps/placeholder_engine/` |
| Generazione questionario dinamico | `questionnaire` | `apps/questionnaire/` |
| Compilazione con dati mock + risposte | `compiler` | `apps/compiler/` |
| Profilo azienda (futuro) | `accounts` | `apps/accounts/` |
| LLM client unificato | `core` | `core/llm/` |
| Parsing DOCX/PDF comuni | `core` | `core/documents/` |

### LLM Provider
**Scelta**: OpenRouter (non LiteLLm generico)
**Rationale**: Accesso unificato a multipli modelli LLM via singola API. Wrapper in `core/llm/client.py` usa OpenRouter come backend.

### Complete Project Directory Structure

```
ai_tender/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── __init__.py
│   ├── pipeline/                    # Orchestrazione flusso completo
│   │   ├── __init__.py
│   │   ├── models.py                # ProcessingJob (stato JSON)
│   │   ├── views.py                 # Upload, process, download
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── services.py              # Orchestration logic
│   │   ├── utils.py
│   │   ├── tests/
│   │   └── templates/pipeline/
│   ├── document_parser/             # Step 1: Estrazione
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── utils.py
│   │   └── tests/
│   ├── field_analyzer/              # Step 2: Analisi LLM
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── prompts.py
│   │   ├── utils.py
│   │   └── tests/
│   ├── placeholder_engine/          # Step 3: Placeholder
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── registry.py
│   │   ├── utils.py
│   │   └── tests/
│   ├── questionnaire/               # Step 4: Questionario
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── forms.py
│   │   ├── tests/
│   │   └── templates/questionnaire/
│   ├── compiler/                    # Step 5: Compilazione
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── loader.py
│   │   ├── validators.py
│   │   └── tests/
│   └── accounts/                    # Futuro: multi-tenant
│       ├── models.py
│       └── tests/
│
├── core/
│   ├── __init__.py
│   ├── llm/                         # Client OpenRouter
│   │   ├── __init__.py
│   │   ├── client.py                # Wrapper OpenRouter API
│   │   ├── providers.py             # Config OpenRouter
│   │   └── exceptions.py
│   ├── documents/                   # Parser DOCX/PDF
│   │   ├── __init__.py
│   │   ├── docx_parser.py
│   │   ├── pdf_parser.py
│   │   └── exceptions.py
│   ├── exceptions.py
│   ├── validators.py
│   ├── logging.py
│   └── middleware.py
│
├── templates/
│   ├── base.html
│   ├── navbar.html
│   └── footer.html
│
├── static/
│   ├── css/base.css
│   └── img/logo.png
│
├── data/
│   └── company_data.json
│
├── tests/
│   ├── __init__.py
│   ├── test_pipeline_e2e.py
│   └── fixtures/
│       ├── sample_disciplinare.docx
│       └── sample_modulo.pdf
│
└── docs/
    ├── setup.md
    ├── pipeline.md
    └── api.md
```

### Integration Boundaries

**Internal Communication:**
```
pipeline (orchestrator)
  ├── chiama document_parser.services.parse_document()
  ├── chiama field_analyzer.services.analyze_fields()
  ├── chiama placeholder_engine.services.insert_placeholders()
  ├── chiama questionnaire.services.generate_questionnaire()
  └── chiama compiler.services.compile_document()
```

**Data Flow:**
```
[DOCX/PDF upload]
  → pipeline.services orchestrate()
    → document_parser: estrae testo
    → field_analyzer (OpenRouter LLM): identifica campi
    → placeholder_engine: inserisce {placeholder}
    → questionnaire: genera form, aspetta risposte
    → compiler: company_data.json + risposte → sostituisce placeholder
    → output: DOCX compilato
```

## Architecture Validation Results

### Coherence Validation ✅

| Check | Stato |
|-------|-------|
| Decision Compatibility | ✅ OK — Python/Django + python-docx + pdfplumber + OpenRouter compatibili |
| Pattern Consistency | ✅ OK — snake_case allineato con struttura Django |
| Structure Alignment | ✅ OK — Moduli mappano esattamente al data flow |
| Contradictory Decisions | ✅ Nessuna |

### Requirements Coverage Validation ✅

**Functional Requirements:**
- ✅ Upload DOCX/PDF → `apps/pipeline/`
- ✅ Estrazione testo + struttura → `apps/document_parser/`
- ✅ Analisi LLM campi compilabili → `apps/field_analyzer/` + `core/llm/`
- ✅ Inserimento placeholder strutturati → `apps/placeholder_engine/`
- ✅ Generazione questionario dinamico → `apps/questionnaire/`
- ✅ Compilazione con dati azienda + risposte → `apps/compiler/` + `data/company_data.json`
- ✅ Output DOCX compilato → python-docx preserva layout

**Non-Functional Requirements:**
- ✅ Velocità < 5 minuti → Processing sincrono, nessuna coda in MVP
- ✅ 100% correttezza campi → `compiler/validators.py` + fallback review manuale
- ✅ Autonomia utente → Questionario guidato
- ✅ Formato output corretto → python-docx preserva layout originale

### Implementation Readiness Validation ✅

- ✅ Decisioni documentate con versioni
- ✅ Patterns completi (naming, struttura, formati)
- ✅ Struttura progetto specifica e completa
- ✅ Integration points definiti
- ✅ Esempi concreti forniti

### Gap Analysis

**Critical Gaps:** Nessuno

**Important Gaps (post-MVP):**
| Gap | Priorità |
|-----|----------|
| Multi-tenant isolation | Post-MVP |
| DRF per API REST | Post-MVP |
| Async processing (Celery) | Post-MVP |

**Nice-to-Have:**
- CI/CD pipeline
- Monitoring/alerting
- Docker per portabilità

### Architecture Completeness Checklist ✅

**Requirements Analysis:**
- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed (Medium-High)
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**Architectural Decisions:**
- [x] Critical decisions documented con versioni
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Performance considerations addressed

**Implementation Patterns:**
- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**Project Structure:**
- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION
**Confidence Level:** HIGH

**Key Strengths:**
- Architettura modulare con chiara separazione responsabilità
- Data flow end-to-end definito e testabile
- Focus su MVP funzionante con estensibilità futura
- Patterns di consistenza per prevenire conflitti tra agenti AI

**Areas for Future Enhancement:**
- Multi-tenant (accounts app)
- API REST (DRF)
- Async processing (Celery)
- Deploy containerizzato (Docker)
lastStep: 8
status: complete
completedAt: '2026-04-05'
