---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments: []
date: 2026-04-03
author: Davide
---

# Product Brief: ai_tender


## Executive Summary

Il progetto **ai_tender** nasce per democratizzare la partecipazione alle gare d'appalto edilizie da parte delle Piccole e Medie Imprese (PMI). Attraverso una pipeline agentica basata su Intelligenza Artificiale, il sistema automatizza la compilazione dei documenti di partecipazione, riducendo drasticamente i costi e i tempi rispetto ai consulenti tradizionali e minimizzando il rischio di esclusione per errori formali.

Il sistema si integrerà in un SaaS più ampio che comprende tool di analisi della gara e parametri di scoring personalizzati, posizionandosi come piattaforma integrata di procurement intelligence.

---

## Core Vision

### Problem Statement

Le PMI del settore edilizio che partecipano a gare d'appalto pubbliche non hanno le competenze per compilare autonomamente i moduli di partecipazione. La compilazione errata porta all'esclusione automatica dalla gara, con perdita di opportunità di business significative.

### Problem Impact

- **Esclusione automatica**: errori formali nella compilazione = perdita immediata della gara
- **Costi proibitivi**: l'alternativa (consulenti esterni) comporta investimenti elevati e tempistiche lunghe
- **Opportunità perse**: le PMI perdono gare per cui sarebbero qualificate a causa di errori formali
- **Competitività ridotta**: le aziende più piccole non possono competere alla pari con le grandi imprese

### Why Existing Solutions Fall Short

- **Consulenti esterni**: costi elevati, tempistiche lunghe, non scalabili per piccole commesse
- **Fai-da-te**: alto rischio di errori, nessuna guida strutturata
- **Software esistenti**: non gestiscono la variabilità dei moduli tra diverse stazioni appaltanti
- **Nessuna soluzione automatizzata**: non risultano sistemi sul mercato che automatizzino end-to-end questo processo

### Proposed Solution

Una pipeline agentica multi-step che:
1. **Analizza il disciplinare** della gara → estrae la lista completa della documentazione richiesta
2. **Analizza i moduli** di partecipazione → inserisce placeholder nei campi compilabili
3. **Genera un questionario** per raccogliere i dati variabili (es. partecipazione singola o ATI)
4. **Compila automaticamente** i documenti sostituendo placeholder con dati azienda + risposte questionario
5. **Restituisce** il documento compilato pronto per la consegna

**Visione futura**: l'utente seleziona la gara di interesse e viene indirizzato solo al questionario per i dati variabili. L'analisi e l'inserimento placeholder avviene automaticamente in background (batch notturno). I risultati intermedi vengono salvati in database e richiamati on-demand.

### Key Differentiators

- **Piattaforma integrata**: non singolo tool ma ecosistema completo (scoring + compilazione)
- **Conoscenza cumulativa**: ogni gara analizzata migliora l'accuratezza del sistema
- **Approccio multi-step adattivo**: ogni fase si adatta alla specifica gara e azienda
- **Gestione dati oggettivi + variabili**: distinzione tra dati anagrafici e scelte strategiche (es. ATI)
- **Posizionamento unico**: "vincere le gare eliminando gli errori" vs "partecipare alle gare"


## Target Users

### Primary Users

**Profilo: Responsabile Amministrativo PMI Edile**

- Lavora nel settore edilizio con competenze tecniche di cantiere ma limitata esperienza con documentazione amministrativa complessa
- Gestisce 30-40 partecipazioni a gare d'appalto all'anno
- Utilizza portali centralizzati per la scoperta delle gare disponibili
- Non ha accesso a risorse interne per la compilazione professionale dei documenti
- L'alternativa attuale (consulenti esterni) è percepita come costosa e lenta

**Obiettivo**: Partecipare a più gare con minor rischio di esclusione per errori formali, senza dover diventare esperto di documentazione amministrativa.

### Secondary Users

*N/A per questa fase del progetto. Il SaaS finale supporterà anche utenti avanzati e consulenti multi-azienda, ma il focus iniziale è sul compilatore documentale.*

### User Journey

1. **Scoperta gara**: Identifica la gara su portale centralizzato
2. **Caricamento documenti**: Carica disciplinare e moduli su ai_tender
3. **Elaborazione automatica**: Sistema analizza requisiti e inserisce placeholder (futuro: batch notturno automatico)
4. **Compilazione questionario**: Risponde a domande su dati variabili (es. ATI, subappalto)
5. **Output compilato**: Riceve documenti pronti per la consegna
6. **Invio partecipazione**: Verifica rapida e invio alla stazione appaltante


## MVP Scope

### Core Features

#### 1. Analisi Disciplinare (Estrazione Documentazione)
- Input: disciplinare della gara (PDF o DOCX)
- Elaborazione: LLM (via OpenRouter) estrae la lista completa di documenti richiesti per la partecipazione
- Output: checklist strutturata presentata all'utente (limitata alla documentazione amministrativa)

#### 2. Analisi Modulo e Inserimento Placeholder
- Input: documento principale da compilare (PDF o DOCX)
- Elaborazione: LLM analizza il documento, identifica i campi compilabili e inserisce placeholder (es. {ragione_sociale}, {partita_iva})
- Output: documento modificato con placeholder inseriti

#### 3. Generazione Questionario Dati Variabili
- Input: risultato dell'analisi modulo (placeholder individuati)
- Elaborazione: il sistema identifica quali placeholder richiedono dati variabili (non presenti nel profilo utente) e genera un questionario dinamico
- Output: pagina web con lista di domande variabili (numero e contenuto dipendono dalla gara specifica)

#### 4. Compilazione Automatica Documento
- Input: documento con placeholder + dati profilo utente (da database) + risposte questionario
- Elaborazione: sostituzione dei placeholder con i valori corretti
- Output: documento finale compilato, stesso formato dell'originale (PDF o DOCX), pronto per il download

#### 5. Gestione Profilo Utente
- Dati azienda (ragione sociale, P.IVA, sede legale, ecc.) salvati nel profilo utente su database
- Utilizzati automaticamente per i placeholder relativi a dati oggettivi
- Gestiti separatamente dai dati variabili (questionario)

### Out of Scope for MVP

- Integrazione automatica con portali centralizzati per scoperta gare
- Batch notturno automatico per pre-analisi delle gare
- Database per salvataggio risultati intermedi per riuso futuro
- Sistema di scoring e analisi competitiva della gara
- Gestione utenti avanzati e consulenti multi-azienda
- Integrazione con sistemi di firma digitale

### Future Vision

- Selezione gara diretta dal portale (senza caricamento manuale)
- Pre-analisi notturna automatica delle nuove gare disponibili
- Salvataggio in database dei risultati intermedi per ottimizzazione progressiva
- Integrazione completa con tool di scoring personalizzato
- Piattaforma SaaS completa di procurement intelligence
