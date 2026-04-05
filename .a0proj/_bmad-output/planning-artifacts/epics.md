---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics]
inputDocuments:
  - prd.md
  - architecture.md
  - product-brief-ai_tender-2026-04-03.md
---

# ai_tender - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for ai_tender, decomposing the requirements from the PRD and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

- FR1: L'utente puo caricare documenti in formato PDF (nativo o scannerizzato)
- FR2: L'utente puo caricare documenti in formato DOCX
- FR3: Il sistema puo eseguire OCR su PDF scannerizzati per estrarre il contenuto testuale
- FR4: Il sistema puo parsare il contenuto dei documenti PDF nativi
- FR5: Il sistema puo parsare il contenuto dei documenti DOCX
- FR6: Il sistema puo analizzare il disciplinare di gara (PDF/DOCX) tramite LLM
- FR7: Il sistema puo estrarre la lista completa dei documenti richiesti per la partecipazione
- FR8: Il sistema puo presentare all'utente una checklist strutturata dei documenti richiesti
- FR9: Il sistema puo identificare i campi compilabili nei moduli di partecipazione
- FR10: Il sistema puo inserire placeholder strutturati (es. {ragione_sociale}, {partita_iva}) nei campi compilabili
- FR11: Il sistema puo gestire caselle di testo come placeholder
- FR12: Il sistema puo identificare le checkbox nei moduli e generare domande corrispondenti nel questionario
- FR13: Il sistema puo identificare i dropdown nei moduli e generare domande a scelta multipla
- FR14: Il sistema puo identificare i campi data e gestirli con formato standard
- FR15: Il sistema puo rilevare sezioni nuove o inaspettate nei moduli
- FR16: Il sistema puo generare un modulo di richiesta informazioni per raccogliere DATI VARIABILI non risolvibili dal profilo utente
- FR17: Il sistema puo distinguere tra dati oggettivi (da profilo utente) e dati variabili (da raccogliere contestualmente)
- FR18: Il questionario puo gestire scelte a opzioni e campi liberi per dati variabili
- FR19: Il sistema puo validare le risposte dell'utente prima della compilazione
- FR20: Il sistema puo sostituire i placeholder con i dati del profilo utente
- FR21: Il sistema puo sostituire i placeholder con le risposte al questionario (dati variabili)
- FR22: Il sistema puo compilare le checkbox in base alle risposte fornite
- FR23: Il sistema puo preservare il layout e il formato del documento originale nell'output
- FR24: L'utente puo scaricare il documento compilato nello stesso formato di input (PDF->PDF, DOCX->DOCX)
- FR25: L'utente puo creare un profilo aziendale (ragione sociale, P.IVA, sede legale, ecc.)
- FR26: Il sistema puo salvare i dati azienda per riuso futuro
- FR27: Il sistema puo riutilizzare automaticamente i dati del profilo per i placeholder corrispondenti
- FR28: L'utente puo modificare il proprio profilo aziendale
- FR29: Il sistema puo garantire isolamento dati tra tenant (ogni PMI accede solo ai propri dati)
- FR30: L'utente puo accedere al proprio spazio tramite autenticazione (email/password)

### NonFunctional Requirements

- NFR1: Elaborazione documento completo: < 2 minuti
- NFR2: OCR + parsing PDF scannerizzato: < 3 minuti
- NFR3: Tempo risposta questionario: < 1 secondo
- NFR4: Dati azienda (P.IVA, bilanci) criptati at rest con AES-256
- NFR5: Documenti upload/processati criptati in transit con TLS 1.2+
- NFR6: Isolamento dati tra tenant con zero cross-tenant data leakage verificabile tramite penetration testing
- NFR7: Autenticazione sicura (email/password con hashing bcrypt + session management con timeout 30 minuti)
- NFR8: Uptime: 99.5%
- NFR9: Backup giornaliero documenti e profili utente con retention di 30 giorni e recovery testabile entro 1 ora
- NFR10: Recovery time: < 1 ora in caso di failure

### Additional Requirements

- Starter template Django greenfield (deciso in architecture)
- Struttura modulare: core/llm/, apps/pipeline/, apps/document_parser/, apps/field_analyzer/, apps/questionnaire/, apps/compiler/
- Logging multi-livello (DEBUG/INFO/WARNING/ERROR/CRITICAL)
- Eccezioni custom: DocumentParseError, FieldAnalysisError, CompilationError
- Messaggi utente friendly, in italiano, senza stack trace
- Fallback: campi non riconosciuti -> marcati per review manuale
- LLM provider: OpenRouter (LiteLLM client unificato)
- Backend: Python + Django
- Test-Driven Development (TDD) obbligatorio
- Configurazione via environment variables (variables.env, secrets.env)

### FR Coverage Map

FR1: Epic 2 - Upload e Analisi Disciplinare (caricamento PDF)
FR2: Epic 2 - Upload e Analisi Disciplinare (caricamento DOCX)
FR3: Epic 2 - Upload e Analisi Disciplinare (OCR PDF scannerizzati)
FR4: Epic 2 - Upload e Analisi Disciplinare (parsing PDF nativi)
FR5: Epic 2 - Upload e Analisi Disciplinare (parsing DOCX)
FR6: Epic 2 - Upload e Analisi Disciplinare (analisi LLM disciplinare)
FR7: Epic 2 - Upload e Analisi Disciplinare (estrazione lista documenti richiesti)
FR8: Epic 2 - Upload e Analisi Disciplinare (checklist strutturata)
FR9: Epic 3 - Analisi Moduli e Placeholder (identificazione campi compilabili)
FR10: Epic 3 - Analisi Moduli e Placeholder (inserimento placeholder strutturati)
FR11: Epic 3 - Analisi Moduli e Placeholder (caselle di testo)
FR12: Epic 3 - Analisi Moduli e Placeholder (checkbox -> questionario)
FR13: Epic 3 - Analisi Moduli e Placeholder (dropdown -> scelta multipla)
FR14: Epic 3 - Analisi Moduli e Placeholder (campi data)
FR15: Epic 3 - Analisi Moduli e Placeholder (sezioni nuove/inaspettate)
FR16: Epic 4 - Questionario Dinamico (generazione modulo dati variabili)
FR17: Epic 4 - Questionario Dinamico (distinzione dati oggettivi/variabili)
FR18: Epic 4 - Questionario Dinamico (gestione scelte opzioni e campi liberi)
FR19: Epic 4 - Questionario Dinamico (validazione risposte)
FR20: Epic 5 - Compilazione e Download (sostituzione placeholder profilo)
FR21: Epic 5 - Compilazione e Download (sostituzione placeholder questionario)
FR22: Epic 5 - Compilazione e Download (compilazione checkbox)
FR23: Epic 5 - Compilazione e Download (preservazione layout originale)
FR24: Epic 5 - Compilazione e Download (download formato originale)
FR25: Epic 1 - Autenticazione e Profilo (creazione profilo aziendale)
FR26: Epic 1 - Autenticazione e Profilo (salvataggio dati azienda)
FR27: Epic 1 - Autenticazione e Profilo (riuso automatico dati profilo)
FR28: Epic 1 - Autenticazione e Profilo (modifica profilo aziendale)
FR29: Epic 1 - Autenticazione e Profilo (isolamento dati tenant)
FR30: Epic 1 - Autenticazione e Profilo (autenticazione email/password)

## Epic List

### Epic 1: Autenticazione e Gestione Profilo Aziendale
Gli utenti possono registrarsi, autenticarsi e gestire i dati della propria azienda. Il sistema garantisce isolamento dati tra tenant.
**FRs covered:** FR25, FR26, FR27, FR28, FR29, FR30
**NFRs:** NFR4 (AES-256), NFR5 (TLS 1.2+), NFR6 (zero cross-tenant), NFR7 (bcrypt auth)

### Epic 2: Upload e Analisi Disciplinare di Gara
Gli utenti possono caricare il disciplinare della gara (PDF/DOCX) e il sistema lo analizza tramite LLM per estrarre la lista completa dei documenti richiesti per la partecipazione, presentando una checklist strutturata.
**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8
**NFRs:** NFR1 (< 2 min elaborazione), NFR2 (< 3 min OCR)
**Nota:** Il disciplinare e il documento PDF che descrive la gara e indica quali documenti servono.

### Epic 3: Analisi Moduli di Partecipazione e Inserimento Placeholder
Il sistema analizza i moduli di partecipazione (DOCX) caricati dall'utente, identifica tutti i campi compilabili (testo, checkbox, dropdown, date) e inserisce placeholder strutturati nei campi corrispondenti.
**FRs covered:** FR9, FR10, FR11, FR12, FR13, FR14, FR15
**Nota:** I moduli sono documenti separati dal disciplinare - sono i file DOCX da compilare con i dati dell'azienda.

### Epic 4: Questionario Dinamico e Raccolta Dati Variabili
Il sistema genera un questionario personalizzato per raccogliere i dati variabili non presenti nel profilo aziendale (es. modalita partecipazione ATI/RTI, subappalto, importo offerto), distinguendo tra dati oggettivi e contestuali.
**FRs covered:** FR16, FR17, FR18, FR19
**NFRs:** NFR3 (< 1 sec risposta questionario)

### Epic 5: Compilazione Automatica e Download Documenti
Il sistema compila automaticamente i documenti sostituendo i placeholder con i dati del profilo aziendale e le risposte al questionario, preservando il layout originale e permettendo il download nello stesso formato di input.
**FRs covered:** FR20, FR21, FR22, FR23, FR24


## Epic 1: Autenticazione e Gestione Profilo Aziendale

Gli utenti possono registrarsi, autenticarsi e gestire i dati della propria azienda. Il sistema garantisce isolamento dati tra tenant.

### Story 1.1: Setup Django Project e Configurazione Base

As a developer,
I want il progetto Django configurato con la struttura modulare definita in architecture,
So that posso iniziare a sviluppare le funzionalità su una base solida.

**Acceptance Criteria:**

**Given** il repository del progetto è vuoto
**When** eseguo il setup iniziale
**Then** il progetto Django è creato con la struttura: core/llm/, apps/pipeline/, apps/document_parser/, apps/field_analyzer/, apps/questionnaire/, apps/compiler/
**And** la configurazione usa environment variables (variables.env, secrets.env)
**And** il logging è configurato con livelli DEBUG/INFO/WARNING/ERROR/CRITICAL
**And** le eccezioni custom sono definite: DocumentParseError, FieldAnalysisError, CompilationError

### Story 1.2: Registrazione Utente con Email

As a responsabile amministrativo di una PMI edile,
I want registrarmi con email e password,
So that posso creare un account per accedere alla piattaforma.

**Acceptance Criteria:**

**Given** l'utente non ha un account
**When** inserisce email e password nel form di registrazione
**Then** l'account viene creato con password hashata con bcrypt
**And** l'utente riceve conferma della registrazione
**And** il tenant viene creato con isolamento dati garantito (NFR6)

### Story 1.3: Login e Session Management

As a utente registrato,
I want accedere con le mie credenziali,
So that posso utilizzare la piattaforma in modo sicuro.

**Acceptance Criteria:**

**Given** l'utente ha un account attivo
**When** inserisce email e password valide
**Then** la sessione viene creata con timeout di 30 minuti (NFR7)
**And** i dati sono protetti in transit con TLS 1.2+ (NFR5)
**And** l'utente è reindirizzato alla dashboard

### Story 1.4: Creazione Profilo Aziendale

As a utente autenticato,
I want inserire i dati della mia azienda (ragione sociale, P.IVA, sede legale),
So that il sistema può utilizzarli per compilare i documenti.

**Acceptance Criteria:**

**Given** l'utente è autenticato e non ha un profilo aziendale
**When** inserisce i dati aziendali (ragione sociale, P.IVA, sede legale, etc.)
**Then** il profilo viene salvato nel database (FR25, FR26)
**And** i dati sensibili (P.IVA, bilanci) sono criptati at rest con AES-256 (NFR4)
**And** i dati sono associati al tenant dell'utente

### Story 1.5: Modifica Profilo Aziendale

As a utente con profilo aziendale,
I want modificare i dati della mia azienda,
So that le informazioni sono sempre aggiornate per le compilazioni future.

**Acceptance Criteria:**

**Given** l'utente ha un profilo aziendale esistente
**When** modifica uno o più campi del profilo
**Then** le modifiche vengono salvate (FR28)
**And** i dati aggiornati saranno utilizzati nelle prossime compilazioni (FR27)


## Epic 2: Upload e Analisi Disciplinare di Gara

Gli utenti possono caricare il disciplinare della gara (PDF/DOCX) e il sistema lo analizza tramite LLM per estrarre la lista completa dei documenti richiesti.

### Story 2.1: Upload File PDF e DOCX

As a responsabile amministrativo,
I want caricare un file PDF o DOCX (il disciplinare di gara),
So that il sistema può analizzarlo per identificare i documenti richiesti.

**Acceptance Criteria:**

**Given** l'utente è autenticato e ha un profilo aziendale
**When** seleziona e carica un file PDF o DOCX
**Then** il file viene salvato nel sistema associato al tenant dell'utente
**And** il sistema conferma il caricamento con nome file e dimensione
**And** il formato del file viene validato (solo PDF o DOCX accettati)

### Story 2.2: Parsing PDF Nativo

As a sistema,
I want estrarre il contenuto testuale da un PDF nativo caricato,
So that il contenuto è disponibile per l'analisi LLM.

**Acceptance Criteria:**

**Given** un file PDF nativo è stato caricato
**When** il sistema esegue il parsing
**Then** il contenuto testuale viene estratto correttamente (FR4)
**And** il parsing completa in meno di 2 minuti (NFR1)
**And** se il parsing fallisce, l'utente riceve un messaggio di errore friendly in italiano

### Story 2.3: OCR su PDF Scannerizzati

As a sistema,
I want eseguire OCR su PDF scannerizzati per estrarre il contenuto testuale,
So that anche i disciplinari cartacei scansionati possono essere analizzati.

**Acceptance Criteria:**

**Given** un file PDF scannerizzato (immagini) è stato caricato
**When** il sistema esegue l'OCR
**Then** il contenuto testuale viene estratto tramite OCR (FR3)
**And** l'OCR completa in meno di 3 minuti (NFR2)
**And** il sistema rileva automaticamente se il PDF è nativo o scannerizzato

### Story 2.4: Parsing Documenti DOCX

As a sistema,
I want parsare il contenuto di documenti DOCX,
So that i disciplinari in formato Word possono essere analizzati.

**Acceptance Criteria:**

**Given** un file DOCX è stato caricato
**When** il sistema esegue il parsing
**Then** il contenuto testuale viene estratto correttamente (FR5)
**And** la struttura del documento (titoli, sezioni, liste) viene preservata
**And** il parsing completa in meno di 2 minuti (NFR1)

### Story 2.5: Analisi LLM del Disciplinare

As a sistema,
I want analizzare il contenuto del disciplinare tramite LLM,
So that posso identificare quali documenti sono richiesti per la partecipazione.

**Acceptance Criteria:**

**Given** il contenuto testuale del disciplinare è stato estratto
**When** il sistema invia il contenuto al LLM (OpenRouter via LiteLLM)
**Then** il LLM analizza il disciplinare ed estrae la lista dei documenti richiesti (FR6, FR7)
**And** il risultato include nome documento e requisiti specifici per ciascuno
**And** il sistema gestisce gracefully eventuali errori del LLM con messaggi in italiano

### Story 2.6: Presentazione Checklist Documenti Richiesti

As a responsabile amministrativo,
I want vedere una checklist strutturata dei documenti richiesti dalla gara,
So that so esattamente cosa devo preparare per partecipare.

**Acceptance Criteria:**

**Given** il LLM ha estratto la lista dei documenti richiesti
**When** l'utente visualizza i risultati dell'analisi
**Then** viene presentata una checklist strutturata con tutti i documenti richiesti (FR8)
**And** ogni voce della checklist mostra il nome del documento
**And** la checklist è scaricabile/stampabile


## Epic 3: Analisi Moduli di Partecipazione e Inserimento Placeholder

Il sistema analizza i moduli di partecipazione (DOCX) caricati dall'utente, identifica tutti i campi compilabili e inserisce placeholder strutturati.

### Story 3.1: Upload Modulo di Partecipazione

As a responsabile amministrativo,
I want caricare il modulo di partecipazione alla gara (file DOCX),
So that il sistema può analizzarlo per identificare i campi da compilare.

**Acceptance Criteria:**

**Given** l'utente ha già visto la checklist documenti dal disciplinare
**When** carica un file DOCX come modulo di partecipazione
**Then** il file viene salvato e associato alla gara corrente
**And** il formato viene validato (solo DOCX accettato per moduli compilabili)
**And** il sistema conferma il caricamento con nome file e dimensione

### Story 3.2: Identificazione Campi Testo Compilabili

As a sistema,
I want identificare i campi di testo vuoti nel modulo DOCX,
So that posso inserire placeholder strutturati per i dati aziendali.

**Acceptance Criteria:**

**Given** un modulo DOCX è stato caricato
**When** il sistema analizza il contenuto del modulo
**Then** vengono identificati tutti i campi di testo compilabili (FR9, FR11)
**And** ogni campo riceve un placeholder strutturato (es. {ragione_sociale}, {partita_iva}) (FR10)
**And** i campi non riconosciuti sono marcati per review manuale (fallback)

### Story 3.3: Identificazione e Gestione Checkbox

As a sistema,
I want identificare le checkbox nel modulo e generare domande corrispondenti,
So that le risposte dell'utente potranno essere usate per compilare le checkbox.

**Acceptance Criteria:**

**Given** un modulo DOCX contiene checkbox
**When** il sistema analizza il modulo
**Then** le checkbox vengono identificate correttamente (FR12)
**And** viene generata una domanda corrispondente per ogni checkbox nel questionario
**And** il placeholder per la checkbox è formattato in modo univoco

### Story 3.4: Identificazione e Gestione Dropdown

As a sistema,
I want identificare i menu a tendina nel modulo e generare domande a scelta multipla,
So that l'utente può selezionare l'opzione corretta per ogni dropdown.

**Acceptance Criteria:**

**Given** un modulo DOCX contiene dropdown (menu a tendina)
**When** il sistema analizza il modulo
**Then** i dropdown vengono identificati con le opzioni disponibili (FR13)
**And** viene generata una domanda a scelta multipla con le stesse opzioni
**And** il placeholder del dropdown indica la selezione da effettuare

### Story 3.5: Gestione Campi Data

As a sistema,
I want identificare i campi data nel modulo e gestirli con formato standard,
So that le date vengono compilate correttamente.

**Acceptance Criteria:**

**Given** un modulo DOCX contiene campi per date
**When** il sistema analizza il modulo
**Then** i campi data vengono identificati (FR14)
**And** il formato della data è gestito come standard (GG/MM/AAAA o come richiesto dal modulo)
**And** il placeholder per la data è {campo_data} con indicazione del formato atteso

### Story 3.6: Rilevamento Sezioni Nuove e Inaspettate

As a responsabile amministrativo,
I want che il sistema mi avvisi se il modulo contiene sezioni nuove o inaspettate,
So that non rischio di essere escluso dalla gara per mancata compilazione.

**Acceptance Criteria:**

**Given** un modulo DOCX è stato analizzato
**When** il sistema incontra una sezione non standard o precedentemente mai vista
**Then** la sezione viene marcata come "nuova" e segnalata all'utente (FR15)
**And** il sistema suggerisce un possibile placeholder o azione da intraprendere
**And** l'utente riceve un avviso chiaro in italiano sulla sezione inaspettata


## Epic 4: Questionario Dinamico e Raccolta Dati Variabili

Il sistema genera un questionario personalizzato per raccogliere i dati variabili non presenti nel profilo aziendale.

### Story 4.1: Distinzione Dati Oggettivi vs Variabili

As a sistema,
I want distinguere tra dati oggettivi (da profilo utente) e dati variabili (da raccogliere contestualmente),
So that il questionario raccoglie solo i dati non già disponibili nel profilo.

**Acceptance Criteria:**

**Given** il sistema ha analizzato i moduli e identificato i placeholder
**When** confronta i placeholder con i dati disponibili nel profilo aziendale
**Then** classifica ogni placeholder come "oggettivo" (proveniente dal profilo) o "variabile" (da raccogliere) (FR17)
**And** genera domande solo per i placeholder classificati come "variabili"

### Story 4.2: Generazione Questionario Dinamico

As a responsabile amministrativo,
I want rispondere a un questionario personalizzato con le domande specifiche per la mia gara,
So that fornisco tutti i dati contestuali necessari per la compilazione.

**Acceptance Criteria:**

**Given** il sistema ha identificato i dati variabili da raccogliere
**When** genera il questionario
**Then** ogni domanda è chiara e in italiano (FR16)
**And** il questionario include domande per: modalità partecipazione (singola/ATI/RTI), subappalto, importo offerto, durata lavori (FR16)
**And** il tempo di risposta per ogni domanda è < 1 secondo (NFR3)

### Story 4.3: Gestione Scelte a Opzioni e Campi Liberi

As a responsabile amministrativo,
I want che il questionario gestisca sia scelte predefinite che campi liberi,
So that posso selezionare da opzioni predefinite o inserire dati specifici quando necessario.

**Acceptance Criteria:**

**Given** il questionario è stato generato
**When** l'utente risponde alle domande
**Then** le domande con opzioni finite mostrano scelte a radio/checkbox (FR18)
**And** le domande con dati non prevedibili mostrano campi di input libero (FR18)
**And** il sistema non blocca l'utente su domande non obbligatorie

### Story 4.4: Validazione Risposte Prima della Compilazione

As a responsabile amministrativo,
I want che il sistema validi le mie risposte prima di procedere alla compilazione,
So that evito errori nei documenti finali.

**Acceptance Criteria:**

**Given** l'utente ha completato il questionario
**When** clicca su "Conferma" o "Procedi"
**Then** il sistema valida tutte le risposte (FR19)
**And** i campi obbligatori sono verificati come non vuoti
**And** i formati numerici (importi, date) sono validati
**And** in caso di errori, il sistema mostra messaggi chiari in italiano per ogni campo non valido


## Epic 5: Compilazione Automatica e Download Documenti

Il sistema compila automaticamente i documenti sostituendo i placeholder con i dati del profilo aziendale e le risposte al questionario.

### Story 5.1: Sostituzione Placeholder con Dati Profilo

As a sistema,
I want sostituire i placeholder nei moduli con i dati del profilo aziendale,
So that i campi oggettivi (ragione sociale, P.IVA, etc.) sono compilati automaticamente.

**Acceptance Criteria:**

**Given** il profilo aziendale è completo e i moduli hanno placeholder inseriti
**When** il sistema esegue la compilazione
**Then** tutti i placeholder corrispondenti ai dati del profilo vengono sostituiti correttamente (FR20)
**And** i dati sostituiti sono coerenti con quelli salvati nel profilo (FR27)
**And** la sostituzione è verificata: nessun placeholder non sostituito rimane per dati del profilo

### Story 5.2: Sostituzione Placeholder con Risposte Questionario

As a sistema,
I want sostituire i placeholder rimanenti con le risposte fornite nel questionario,
So that anche i dati variabili (modalità partecipazione, subappalto, etc.) sono compilati.

**Acceptance Criteria:**

**Given** l'utente ha completato il questionario con le risposte valide
**When** il sistema esegue la compilazione
**Then** i placeholder per i dati variabili vengono sostituiti con le risposte del questionario (FR21)
**And** le risposte a scelta multipla compilano correttamente i dropdown
**And** i campi data sono inseriti nel formato corretto

### Story 5.3: Compilazione Checkbox

As a sistema,
I want compilare le checkbox nei moduli in base alle risposte fornite,
So that le sezioni con opzioni booleane sono correttamente spuntate.

**Acceptance Criteria:**

**Given** il modulo contiene checkbox e l'utente ha fornito risposte corrispondenti
**When** il sistema esegue la compilazione
**Then** le checkbox sono spuntate o lasciate vuote in base alle risposte (FR22)
**And** ogni checkbox è compilata in accordo con la domanda corrispondente nel questionario

### Story 5.4: Preservazione Layout Originale

As a responsabile amministrativo,
I want che il documento compilato mantenga lo stesso layout e formato del documento originale,
So that il risultato è professionale e conforme ai requisiti della gara.

**Acceptance Criteria:**

**Given** il documento originale ha un layout specifico (font, margini, tabelle, immagini)
**When** il sistema esegue la compilazione
**Then** il layout originale è preservato nell'output (FR23)
**And** i font, margini, spaziature e allineamenti rimangono invariati
**And** le tabelle e immagini non sono deformate o spostate

### Story 5.5: Download Documento Compilato

As a responsabile amministrativo,
I want scaricare il documento compilato nello stesso formato di input,
So that posso inviarlo direttamente per la partecipazione alla gara.

**Acceptance Criteria:**

**Given** la compilazione è completata con successo
**When** l'utente clicca su "Scarica" o "Download"
**Then** il documento viene scaricato nello stesso formato dell'input: PDF→PDF, DOCX→DOCX (FR24)
**And** il file scaricato è apribile e visualizzabile correttamente
**And** il nome del file indica che è il documento compilato (es. suffisso "_compilato")
