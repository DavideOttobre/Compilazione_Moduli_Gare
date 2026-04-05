---
stepsCompleted: [step-01-init, step-02-discovery, step-02b-vision, step-02c-executive-summary, step-03-success, step-04-journeys, step-05-domain, step-06-innovation, step-07-project-type, step-08-scoping, step-09-functional, step-10-nonfunctional, step-11-polish, step-12-complete]
inputDocuments:
  - product-brief-ai_tender-2026-04-03.md
workflowType: 'prd'
date: 2026-04-03
author: Davide
classification:
  projectType: SaaS B2B + AI/Automation
  domain: GovTech / Procurement
  complexity: Medium-High
  projectContext: greenfield
vision:
  statement: Democratizzare la partecipazione alle gare d'appalto edilizie, permettendo alle PMI di compilare autonomamente e rapidamente la documentazione amministrativa, eliminando la dipendenza da consulenti esterni.
  differentiator: Velocita (pochi minuti) + Semplicita (poco sforzo) + Indipendenza (niente consulenti)
  coreInsight: I modelli LLM hanno raggiunto la maturita per l'analisi documentale complessa. Il mercato e maturo e affascinato dall'AI.
  futureState: Autonomia, tempo risparmiato, piu partecipazioni, minor rischio, risparmio costi
---

# Product Requirements Document - ai_tender

**Author:** Davide
**Date:** 2026-04-03

## Executive Summary

**ai_tender** e una piattaforma SaaS B2B basata su AI che automatizza la compilazione dei documenti di partecipazione alle gare d'appalto edilizie per le Piccole e Medie Imprese (PMI).

### Problema
Le PMI del settore edilizio che partecipano a gare d'appalto pubbliche non hanno le competenze per compilare autonomamente i moduli di partecipazione. La compilazione errata porta all'esclusione automatica dalla gara, con perdita di opportunità di business significative. L'alternativa attuale — consulenti esterni — comporta costi elevati e tempistiche lunghe non scalabili per piccole commesse.

### Soluzione
Una pipeline agentica multi-step che analizza il disciplinare della gara, identifica i campi compilabili nei moduli, inserisce placeholder strutturati, genera un questionario dinamico per i dati variabili e compila automaticamente i documenti sostituendo i placeholder con i dati azienda e le risposte al questionario.

### Target
Responsabile Amministrativo delle PMI Edili — professionisti con competenze tecniche di cantiere ma limitata esperienza con documentazione amministrativa complessa, che gestiscono 30-40 partecipazioni a gare all'anno.

## What Makes This Special

### Differentiatori Chiave
- **Velocita**: Documento compilato in pochi minuti, non giorni o settimane
- **Semplicita**: Carica i documenti, rispondi al questionario, scarica il risultato — zero complessita
- **Indipendenza**: Elimina la dipendenza da consulenti esterni, costi e attese
- **Conoscenza cumulativa**: Ogni gara analizzata migliora l'accuratezza del sistema
- **Approccio adattivo**: Ogni fase si adatta alla specifica gara e azienda

### Core Insight
I modelli LLM hanno raggiunto la maturita necessaria per l'analisi documentale complessa. Il mercato e maturo e affascinato dall'AI — le PMI sono pronte ad adottare soluzioni intelligenti per automatizzare processi burocratici complessi.

### Vision
Democratizzare la partecipazione alle gare d'appalto edilizie, permettendo alle PMI di compilare autonomamente e rapidamente la documentazione amministrativa, eliminando la dipendenza da consulenti esterni e riducendo il rischio di esclusione per errori formali.

## Project Classification

| Classificazione | Valore |
|-----------------|--------|
| **Project Type** | SaaS B2B + AI/Automation |
| **Domain** | GovTech / Procurement |
| **Complexity** | Medium-High |
| **Project Context** | Greenfield |

## Success Criteria

### User Success

| Criterio | Metrica |
|----------|---------|
| **Velocita** | Documento compilato in **< 5 minuti** (vs giorni/settimane con consulente) |
| **Correttezza** | **100%** dei campi compilati correttamente, zero errori formali |
| **Autonomia** | L'utente completa l'intero processo **senza assistenza esterna** |
| **Formato** | Output finale con layout e contenuto corretti |

**Momento AHA**: *"Il documento e pronto, corretto e formattato — in meno tempo di quanto impieghi a bere un caffe."*

### Business Success

| Timeframe | Metrica | Target |
|-----------|---------|--------|
| **3 mesi** | Utenti attivi (paying) | 20-30 PMI |
| **6 mesi** | MRR (Monthly Recurring Revenue) | Milestone intermedie verso break-even |
| **12 mesi** | Documenti compilati/mese | 500+ |
| **12 mesi** | Churn rate | < 5% |

**Metrica chiave**: **Revenue** — il prodotto e valido se le PMI pagano per usarlo.

### Technical Success

| Criterio | Requisito |
|----------|-----------|
| **Accuratezza identificazione** | >= 90% dei campi identificati correttamente nei moduli |
| **Accuratezza compilazione** | 100% sostituzione placeholder senza errori |
| **Formati supportati** | PDF e DOCX (input e output) |
| **Velocita elaborazione** | < 2 minuti per documento completo |
| **Disponibilita** | 99.5% uptime |

## Product Scope

### MVP - Minimum Viable Product

> *"Documenti compilati per intero, correttamente e formattati correttamente."*

| Feature | Descrizione |
|---------|-------------|
| **1. Analisi Disciplinare** | LLM estrae lista documenti richiesti dal disciplinare (PDF/DOCX) |
| **2. Analisi Modulo + Placeholder** | LLM identifica campi compilabili e inserisce placeholder strutturati |
| **3. Questionario Dinamico** | Generazione domande per dati variabili (es. ATI, subappalto) |
| **4. Compilazione Automatica** | Sostituzione placeholder con dati profilo + risposte questionario |
| **5. Gestione Profilo Utente** | Dati azienda salvati e riutilizzati automaticamente |

### Growth Features (Post-MVP)

| Feature | Descrizione |
|---------|-------------|
| Integrazione portali gare | Scoperta automatica gare da portali centralizzati |
| Batch notturno | Pre-analisi automatica nuove gare disponibili |
| Database risultati | Salvataggio e riuso risultati intermedi |
| Multi-azienda | Supporto consulenti che gestiscono piu PMI |

### Vision (Future)

| Feature | Descrizione |
|---------|-------------|
| Procurement Intelligence | Piattaforma completa con analisi, scoring e compilazione |
| Scoring competitivo | Analisi probabilita vittoria gara |
| Firma digitale | Integrazione firme elettroniche |

## User Journeys

### Persona: Marco — Responsabile Amministrativo PMI Edile

- Competenze tecniche di cantiere, limitata esperienza documentazione amministrativa
- Gestisce 30-40 partecipazioni a gare d'appalto all'anno
- Obiettivo: partecipare a piu gare con minor rischio di esclusione

### Journey 1: La Prima Gara Senza Consulente

**Opening Scene**: Marco trova una gara per la ristrutturazione di una scuola comunale (€500K). Deadline tra 5 giorni. Il consulente e in ferie.

**Rising Action**:
1. Scarica disciplinare (15 pagine) e 3 moduli
2. Sa che compilare manualmente richiede 2-3 giorni
3. Un collega gli consiglia ai_tender
4. Crea account, inserisce dati azienda, carica documenti
5. Il sistema elabora...

**Climax**: Dopo 3 minuti, i documenti sono pronti. Tutti i campi compilati correttamente, incluse sezioni complesse (subappalto, ATI).

**Resolution**: Tempo totale: 15 minuti invece di 3 giorni. Nessun consulente pagato. Si sente autonomo e sicuro.

**Capacita rivelate**: Upload documenti, Analisi automatica, Questionario dinamico, Profilo utente, Output scaricabile

### Journey 2: L'Errore Evitato

**Persona**: Lucia — Titolare PMI Edile, 15 dipendenti, 5 usi precedenti di ai_tender

**Opening Scene**: Lucia compila una gara. Il modulo ha una sezione nuova: "Dichiarazione antimafia" — mai vista prima.

**Rising Action**:
1. Carica documenti su ai_tender
2. Il sistema identifica la sezione nuova e inserisce placeholder {dichiarazione_antimafia}
3. Genera domanda specifica per la dichiarazione
4. Lucia non sapeva che servisse

**Climax**: Invia i documenti. Confermata la partecipazione valida. Senza ai_tender sarebbe stata esclusa.

**Resolution**: Lucia diventa avvocata del prodotto tra le PMI della sua zona.

**Capacita rivelate**: Rilevamento automatico sezioni nuove, Guida contestuale, Gestione edge cases

### Journey 3: L'Admin della Piattaforma

**Persona**: Andrea — CTO della startup ai_tender

**Opening Scene**: 3 mesi dal lancio, 25 PMI attive. Andrea monitora la salute del sistema.

**Rising Action**:
1. Accede alla dashboard admin
2. Alert: accuratezza scesa all'85% su un formato PDF specifico
3. Identifica formato nuovi moduli non parsato correttamente
4. Aggiorna modello LLM

**Climax**: Giorno dopo, accuratezza tornata al 95%. Nessun utente ha notato il problema.

**Resolution**: "Sistema stabile. Possiamo scalare a 100 PMI."

**Capacita rivelate**: Dashboard admin, Monitoring accuratezza, Alert system, Gestione modelli LLM

### Journey Requirements Summary

| Capacita | Journey 1 | Journey 2 | Journey 3 |
|----------|-----------|-----------|-----------|
| Upload documenti (PDF/DOCX) | ✅ | ✅ | — |
| Analisi disciplinare (LLM) | ✅ | ✅ | — |
| Inserimento placeholder | ✅ | ✅ | — |
| Questionario dinamico | ✅ | ✅ | — |
| Gestione profilo utente | ✅ | ✅ | — |
| Output compilato scaricabile | ✅ | ✅ | — |
| Rilevamento sezioni nuove | — | ✅ | — |
| Guida contestuale | — | ✅ | — |
| Dashboard admin | — | — | ✅ |
| Monitoring accuratezza | — | — | ✅ |
| Alert system | — | — | ✅ |

## Domain-Specific Requirements

### Formati di Input

| Formato | Requisito |
|---------|-----------|
| **PDF nativo** | Parsing testo diretto, estrazione campi compilabili |
| **PDF scannerizzato** | OCR obbligatorio per estrazione contenuto |
| **DOCX** | Parsing XML interno per identificazione campi |

### Gestione Campi Complessi

| Tipo Campo | Gestione MVP |
|------------|--------------|
| **Caselle testo** | Placeholder → sostituzione diretta |
| **Checkbox** | Identificazione nel modulo → domanda nel questionario → spunta automatica |
| **Dropdown** | Identificazione opzioni → domanda a scelta multipla nel questionario |
| **Date** | Formato standard → inserimento automatico |
| **Firme** | Out of scope per MVP (firma digitale = future) |

### Multi-Documento

| Fase | Comportamento |
|------|---------------|
| **MVP** | Un modulo alla volta — l'utente carica e compila un singolo documento |
| **Future** | Multi-compilazione contemporanea — carica tutti i moduli, compila tutti insieme |

### Pipeline Requirements

| Requisito | Priorita | Note |
|-----------|----------|------|
| OCR per PDF scannerizzati | Must have | Necessario per stazioni appaltanti con moduli cartacei |
| Gestione checkbox via questionario | Must have | Le checkbox devono riflettere le risposte utente |
| Preservazione layout output | Must have | Output deve mantenere formato e layout originale |
| Parsing multi-formato (PDF + DOCX) | Must have | Entrambi i formati supportati come input |
| Compilazione singolo modulo | Must have | MVP: un modulo alla volta |
| Compilazione multi-modulo | Future | Post-MVP: batch multipli documenti |

## Innovation & Novel Patterns

### Detected Innovation Areas

| Area | Dettaglio |
|------|-----------|
| **Nessun concorrente end-to-end** | Non risultano sistemi sul mercato che automatizzino end-to-end questo processo |
| **AI Agents per documenti** | Primo uso di pipeline agentica LLM per compilazione documenti amministrativi |
| **Combinazione unica** | AI + Procurement + Edilizia = nicchia inesplorata |
| **Conoscenza cumulativa** | Ogni gara analizzata migliora il sistema — network effect progressivo |

### Market Context & Competitive Landscape

- **Consulenti esterni**: soluzione attuale, costosa e non scalabile
- **Software esistenti**: non gestiscono la variabilità dei moduli tra stazioni appaltanti
- **ai_tender**: unica soluzione automatizzata che combina LLM + procurement + edilizia

### Validation Approach

| Metodo | Obiettivo |
|--------|-----------|
| **Dataset benchmark** | 10-20 documenti reali di gare d'appalto per test accuratezza |
| **Beta testing** | 20-30 PMI nei primi 3 mesi per validare UX e risultati |
| **Monitoring continuo** | Dashboard accuratezza con alert per degradazione |

### Risk Mitigation

| Rischio | Mitigazione |
|---------|-------------|
| Accuratezza variabile su formati nuovi | Dataset benchmark + aggiornamento modelli |
| Resistenza all'adozione PMI | UX ultra-semplice, primo utilizzo gratuito |
| Stazioni appaltanti cambiano formati | Sistema adattivo + knowledge cumulativa |

## SaaS B2B Specific Requirements

### Tenant Model

- Ogni PMI ha uno spazio isolato con dati separati
- Profilo aziendale e documenti separati per utente
- Authentication base (email/password)

### Skipped Sections (non rilevanti per MVP)

- Subscription tiers, RBAC complesso, mobile-first, CLI interface

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Problem-Solving MVP — documenti compilati per intero, correttamente e formattati correttamente.

### MVP Feature Set (Phase 1) — Core Pipeline

| # | Feature | Priorita |
|---|---------|----------|
| 1 | Upload documenti (PDF/DOCX + OCR) | Must have |
| 2 | Analisi disciplinare (LLM) | Must have |
| 3 | Analisi modulo + inserimento placeholder | Must have |
| 4 | Questionario dinamico (incluse checkbox) | Must have |
| 5 | Compilazione automatica + output scaricabile | Must have |
| 6 | Gestione profilo utente (dati azienda) | Must have |

### Phase 2 — Growth

| Feature | Priorita |
|---------|----------|
| Compilazione multi-modulo contemporanea | Post-MVP |
| Integrazione portali gare | Post-MVP |
| Batch notturno pre-analisi | Post-MVP |

### Phase 3 — Vision

| Feature | Priorita |
|---------|----------|
| Procurement Intelligence (scoring + analisi) | Vision |
| Firma digitale | Vision |

### Risk Mitigation

| Rischio | Mitigazione |
|---------|-------------|
| Accuratezza LLM su formati variabili | Dataset benchmark 10-20 doc reali + monitoring |
| OCR su PDF scarsi | Test su documenti reali scannerizzati |
| Resistenza adozione PMI | UX ultra-semplice, primo utilizzo gratuito |

## Functional Requirements

### 1. Document Upload & Processing

- FR1: L'utente puo caricare documenti in formato PDF (nativo o scannerizzato)
- FR2: L'utente puo caricare documenti in formato DOCX
- FR3: Il sistema puo eseguire OCR su PDF scannerizzati per estrarre il contenuto testuale
- FR4: Il sistema puo parsare il contenuto dei documenti PDF nativi
- FR5: Il sistema puo parsare il contenuto dei documenti DOCX

### 2. Disciplinare Analysis

- FR6: Il sistema puo analizzare il disciplinare di gara (PDF/DOCX) tramite LLM
- FR7: Il sistema puo estrarre la lista completa dei documenti richiesti per la partecipazione
- FR8: Il sistema puo presentare all'utente una checklist strutturata dei documenti richiesti

### 3. Module Analysis & Placeholder Insertion

- FR9: Il sistema puo identificare i campi compilabili nei moduli di partecipazione
- FR10: Il sistema puo inserire placeholder strutturati (es. {ragione_sociale}, {partita_iva}) nei campi compilabili
- FR11: Il sistema puo gestire caselle di testo come placeholder
- FR12: Il sistema puo identificare le checkbox nei moduli e generare domande corrispondenti nel questionario
- FR13: Il sistema puo identificare i dropdown nei moduli e generare domande a scelta multipla
- FR14: Il sistema puo identificare i campi data e gestirli con formato standard
- FR15: Il sistema puo rilevare sezioni nuove o inaspettate nei moduli

### 4. Dynamic Questionnaire (Informazioni Supplementari)

- FR16: Il sistema puo generare un modulo di richiesta informazioni per raccogliere DATI VARIABILI non risolvibili dal profilo utente (es. modalita di partecipazione singola/ATI/RTI, subappalto, importo offerto, durata lavori, altri dati contestuali specifici della gara)
- FR17: Il sistema può distinguere tra dati oggettivi (da profilo utente) e dati variabili (da raccogliere contestualmente)
- FR18: Il questionario può gestire scelte a opzioni e campi liberi per dati variabili
- FR19: Il sistema può validare le risposte dell'utente prima della compilazione

### 5. Automatic Compilation

- FR20: Il sistema puo sostituire i placeholder con i dati del profilo utente
- FR21: Il sistema puo sostituire i placeholder con le risposte al questionario (dati variabili)
- FR22: Il sistema puo compilare le checkbox in base alle risposte fornite
- FR23: Il sistema puo preservare il layout e il formato del documento originale nell'output
- FR24: L'utente puo scaricare il documento compilato nello stesso formato di input (PDF->PDF, DOCX->DOCX)

### 6. User Profile Management

- FR25: L'utente puo creare un profilo aziendale (ragione sociale, P.IVA, sede legale, ecc.)
- FR26: Il sistema può salvare i dati azienda per riuso futuro
- FR27: Il sistema puo riutilizzare automaticamente i dati del profilo per i placeholder corrispondenti
- FR28: L'utente puo modificare il proprio profilo aziendale

### 7. Tenant Isolation

- FR29: Il sistema può garantire isolamento dati tra tenant (ogni PMI accede solo ai propri dati)
- FR30: L'utente puo accedere al proprio spazio tramite autenticazione (email/password)

## Non-Functional Requirements

### Performance

| NFR | Metrica |
|-----|---------|
| NFR1 | Elaborazione documento completo: < 2 minuti |
| NFR2 | OCR + parsing PDF scannerizzato: < 3 minuti |
| NFR3 | Tempo risposta questionario: < 1 secondo |

### Security

| NFR | Requisito |
|-----|-----------|
| NFR4 | Dati azienda (P.IVA, bilanci) criptati at rest con AES-256 |
| NFR5 | Documenti upload/processati criptati in transit con TLS 1.2+ |
| NFR6 | Isolamento dati tra tenant con zero cross-tenant data leakage verificabile tramite penetration testing |
| NFR7 | Autenticazione sicura (email/password con hashing bcrypt + session management con timeout 30 minuti) |

### Reliability

| NFR | Requisito |
|-----|-----------|
| NFR8 | Uptime: 99.5% |
| NFR9 | Backup giornaliero documenti e profili utente con retention di 30 giorni e recovery testabile entro 1 ora |
| NFR10 | Recovery time: < 1 ora in caso di failure |
