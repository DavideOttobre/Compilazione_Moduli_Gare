---
story_id: "2.5"
title: "Analisi LLM del Disciplinare"
epic: "2 - Upload e Analisi Disciplinare di Gara"
status: "ready-for-dev"
assigned_to: "Amelia"
created_at: "2026-04-11"
updated_at: "2026-04-11"
acceptance_criteria_ref: "epics.md - Story 2.5"
---

# Story 2.5: Analisi LLM del Disciplinare

Status: ready-for-dev

## Story

As a sistema,
I want analizzare il contenuto del disciplinare tramite LLM,
So that posso identificare quali documenti sono richiesti per la partecipazione.

## Acceptance Criteria

1. [AC1] Given il contenuto testuale del disciplinare è stato estratto, When il sistema invia il contenuto al LLM (OpenRouter via LiteLLM), Then il LLM analizza il disciplinare ed estrae la lista dei documenti richiesti (FR6, FR7)
2. [AC2] And il risultato include nome documento e requisiti specifici per ciascuno
3. [AC3] And il sistema gestisce gracefully eventuali errori del LLM con messaggi in italiano
4. [AC4] And solo documenti con status `'parsed'` e campo `parsed_content` non vuoto sono accettati
5. [AC5] And il risultato dell'analisi viene salvato nel modello `RequiredDocument` associato al documento sorgente
6. [AC6] And il `Document.status` viene aggiornato a `'analyzed'` dopo successo o `'error'` su fallimento analisi LLM
7. [AC7] And isolamento tenant: solo documenti dell'utente autenticato sono accessibili
8. [AC8] And l'elaborazione completa in meno di 2 minuti (NFR1)
9. [AC9] And il client LLM unificato in `core/llm/client.py` usa OpenRouter come backend tramite libreria `litellm`
10. [AC10] And il prompt per l'analisi è definito in `apps/field_analyzer/prompts.py` e separato dalla logica di business

## Tasks / Subtasks

- [ ] Task 1: Implementare il client LLM unificato in `core/llm/` (AC: 9)
  - [ ] Creare `core/llm/client.py` con classe/funzione `LLMClient`
  - [ ] Integrare `litellm` per chiamate a OpenRouter
  - [ ] Configurare API key da environment variables (secrets.env)
  - [ ] Implementare metodo `analyze_discipline(content: str, prompt: str) -> dict` per analisi disciplinare
  - [ ] Gestire errori LLM: timeout, rate limit, API errors → `LLMError` custom exception
  - [ ] Logging strutturato per chiamate LLM (DEBUG: prompt, INFO: response, ERROR: failures)
  - [ ] Aggiungere `litellm` a requirements.txt
- [ ] Task 2: Creare modello `RequiredDocument` per salvare risultati analisi (AC: 5)
  - [ ] Definire modello in `apps/field_analyzer/models.py`
  - [ ] Campi: `source_document` (FK a Document), `document_name`, `requirements`, `created_at`
  - [ ] Creare migration
  - [ ] Relazione: un Document → N RequiredDocument
- [ ] Task 3: Implementare prompt di analisi disciplinare (AC: 1, 2, 10)
  - [ ] Creare `apps/field_analyzer/prompts.py` con prompt template
  - [ ] Prompt deve istruire il LLM ad estrarre lista documenti richiesti dal testo del disciplinare
  - [ ] Prompt deve richiedere output strutturato (JSON) con: nome documento, requisiti specifici
  - [ ] Prompt in italiano, con esempi di formato output atteso
  - [ ] Gestire casi edge: disciplinare lungo (chunking se necessario), formato variabile
- [ ] Task 4: Implementare service layer per analisi LLM (AC: 1, 2, 6, 8)
  - [ ] Creare `apps/field_analyzer/services.py` con funzione `analyze_discipline(document)`
  - [ ] Verificare `document.status == 'parsed'` e `document.parsed_content` non vuoto (AC4)
  - [ ] Verificare isolamento tenant: `document.user == request.user` (AC7)
  - [ ] Chiamare `LLMClient.analyze_discipline()` con contenuto estratto
  - [ ] Parsare risposta JSON del LLM e validare formato
  - [ ] Creare record `RequiredDocument` per ogni documento estratto (AC5)
  - [ ] Aggiornare `Document.status` a `'analyzed'` su successo o `'error'` su fallimento (AC6)
  - [ ] Implementare timeout tracking per NFR1 (< 2 min) (AC8)
  - [ ] Gestire errori con messaggi friendly in italiano (AC3)
- [ ] Task 5: Creare endpoint API per trigger analisi LLM (AC: 4, 6, 7)
  - [ ] Creare view `analyze_discipline` in `apps/field_analyzer/views.py`
  - [ ] Accettare solo documenti con `status='parsed'` e `parsed_content` non vuoto (AC4)
  - [ ] Verificare isolamento tenant: `document.user == request.user` (AC7)
  - [ ] Aggiornare `Document.status` a `'analyzed'` o `'error'` (AC6)
  - [ ] Restituire messaggio errore friendly in italiano su fallimento (AC3)
- [ ] Task 6: Aggiornare URL per analisi LLM (AC: 1)
  - [ ] Aggiungere path `field-analyzer/analyze/<int:pk>/` in `apps/field_analyzer/urls.py`
  - [ ] Registrare urls in `ai_tender/urls.py` se non già fatto
- [ ] Task 7: Creare template risultato analisi (AC: 1, 2)
  - [ ] Template `apps/field_analyzer/templates/field_analyzer/analyze_result.html`
  - [ ] Mostrare lista documenti richiesti estratti dal LLM
  - [ ] Mostrare nome documento e requisiti specifici per ciascuno (AC2)
  - [ ] Mostrare errore friendly se analisi fallita
- [ ] Task 8: Test TDD (AC: 1-10)
  - [ ] Test LLM client: chiamata corretta a OpenRouter con prompt (AC9)
  - [ ] Test LLM client: gestione errori (timeout, rate limit, API error) (AC3, AC9)
  - [ ] Test prompt: formato e contenuto corretti del prompt template (AC10)
  - [ ] Test service: analisi documento parsed con successo → RequiredDocument creati (AC1, AC2, AC5)
  - [ ] Test service: rifiuto documenti non in status 'parsed' (AC4)
  - [ ] Test service: rifiuto documenti con parsed_content vuoto (AC4)
  - [ ] Test service: status transition analyzed/error (AC6)
  - [ ] Test service: timeout > 2 min gestito (AC8, NFR1)
  - [ ] Test service: errore LLM con messaggio italiano (AC3)
  - [ ] Test view: endpoint con tenant isolation (AC7)
  - [ ] Test view: response corretta con lista documenti
  - [ ] Test model RequiredDocument: creazione e relazione FK
  - [ ] Test integrazione: flusso completo parsing → analisi → risultato

## Dev Notes

### Architettura e vincoli
- **App destinazione:** `apps/field_analyzer/` — modulo esistente con struttura base (apps.py, models.py, views.py)
- **Nuova dipendenza:** `litellm` per chiamate LLM tramite OpenRouter
- **Modulo core:** `core/llm/` — da popolare con client unificato (attualmente vuoto, solo __init__.py)
- **Pattern LLM:** Client unificato in core/llm/ separa logica LLM da business logic delle singole app
- **Prompt management:** Prompt separati in `prompts.py` per ogni app, non inline nel service layer
- **Output LLM atteso:** JSON strutturato con lista documenti, ognuno con nome e requisiti
- **Status management:** Document status aggiunge nuovo stato `'analyzed'` (transizione: parsed → analyzed o parsed → error)
- **Testing:** TDD obbligatorio. Test per client LLM (mock), service, view, model, prompt
- **NFR1:** Analisi deve completare in < 2 minuti per documento
- **Errori:** Messaggi friendly in italiano, no stack trace esposto (pattern da core/exceptions.py)
- **Isolamento tenant:** Query filtrate per user=request.user (pattern consolidato da Stories 2.1, 2.2, 2.4)

### Configurazione LLM
- **Provider:** OpenRouter (accesso a multipli modelli via singola API)
- **Libreria:** litellm — wrapper unificato per chiamate LLM
- **API Key:** Da `secrets.env` (variabile: `OPENROUTER_API_KEY`)
- **Modello:** Configurabile, default da `variables.env` (es. `OPENROUTER_MODEL=openai/gpt-4o-mini`)
- **Timeout:** Configurabile per chiamata (default: 90s, max totale: 120s per NFR1)
- **Retry:** Opzionale per errori transitori (rate limit, timeout)

### Pattern da Story 2.4 (Parsing DOCX)
- **Service layer:** `apps/document_parser/services.py` → `apps/field_analyzer/services.py` (stesso pattern)
- **View pattern:** stessa struttura della view `parse_docx_document` con check status + tenant isolation
- **Error handling:** usare custom exception `FieldAnalysisError` da `core/exceptions.py` (da aggiungere se non esiste)
- **Status transition:** uploaded → parsed (Story 2.4) vs parsed → analyzed (Story 2.5) — pattern analogo
- **Tests:** stessa struttura dei test in `tests/test_story_2_4.py` ma per analisi LLM con mock del client

### Pattern da Architecture
- **LLM client:** `core/llm/client.py` — wrapper OpenRouter API (decisione architetturale confermata)
- **Struttura modulare:** service + view + template + URL + tests (pattern consistente)
- **Logging:** Multi-livello DEBUG/INFO/WARNING/ERROR/CRITICAL
- **Eccezioni custom:** `FieldAnalysisError`, `LLMError` in `core/exceptions.py`

### Dipendenze Story precedenti
- **Story 1.1:** Setup Django, struttura modulare, eccezioni custom, logging
- **Story 1.2-1.5:** Autenticazione, profilo aziendale, isolamento tenant
- **Story 2.1:** Upload file, Document model, validazione filetype
- **Story 2.2:** Parsing PDF nativo — pattern service/view/status
- **Story 2.4:** Parsing DOCX — pattern TDD, status transition, error handling italiano

### Output LLM atteso (formato JSON)
```json
{
  "documenti_richiesti": [
    {
      "nome": "Dichiarazione di partecipazione",
      "requisiti": "Documento firmato dal legale rappresentante con indicazione della gara"
    },
    {
      "nome": "Visura camerale",
      "requisiti": "Visura camerale aggiornata non oltre 3 mesi dalla data di gara"
    },
    {
      "nome": "DURC",
      "requisiti": "Documento Unico di Regolarità Contributiva in corso di validità"
    }
  ]
}
```

### Project Structure Notes
- File da creare: `core/llm/client.py`, `core/llm/providers.py`, `core/llm/exceptions.py`, `apps/field_analyzer/services.py`, `apps/field_analyzer/prompts.py`, `apps/field_analyzer/urls.py`, template, tests
- File da modificare: `core/exceptions.py` (aggiungere FieldAnalysisError, LLMError), `apps/field_analyzer/models.py` (RequiredDocument), `ai_tender/urls.py` (registrare field_analyzer urls), `requirements.txt` (litellm)
- File test: `tests/test_story_2_5.py` (nuovo)
- Dipendenza: `litellm` da aggiungere a `requirements.txt`

### References
- [Source: planning-artifacts/epics.md#Story 2.5] — Acceptance criteria e user story
- [Source: planning-artifacts/architecture.md#LLM Provider] — OpenRouter via LiteLLM
- [Source: planning-artifacts/architecture.md#Project Structure] — core/llm/ e apps/field_analyzer/
- [Source: planning-artifacts/prd.md#FR6, FR7] — Analisi LLM e estrazione documenti
- [Source: implementation-artifacts/stories/story-2.4-parsing-documenti-docx.md] — Pattern da replicare
- [Source: core/exceptions.py] — Eccezioni custom
- [Source: apps/field_analyzer/models.py] — Modello esistente (base)
- [Source: apps/document_parser/services.py] — Service layer pattern reference

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
