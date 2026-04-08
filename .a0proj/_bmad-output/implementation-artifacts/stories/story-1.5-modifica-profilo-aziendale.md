---
story_id: "1.5"
title: "Modifica Profilo Aziendale"
epic: "1 - Autenticazione e Gestione Profilo Aziendale"
status: "ready-for-dev"
assigned_to: "Amelia"
created_at: "2026-04-06"
updated_at: "2026-04-06"
acceptance_criteria_ref: "epics.md - Story 1.5"
---

# Story 1.5: Modifica Profilo Aziendale

Status: ready-for-dev

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a utente con profilo aziendale,
I want modificare i dati della mia azienda,
So that le informazioni sono sempre aggiornate per le compilazioni future.

## Acceptance Criteria

1. [AC1] Given l'utente ha un profilo aziendale esistente, When modifica uno o più campi del profilo, Then le modifiche vengono salvate (FR28)
2. [AC2] And i dati aggiornati saranno utilizzati nelle prossime compilazioni (FR27)

## Tasks / Subtasks

- [ ] Task 1: Creare view per modifica profilo (AC: 1, 2)
  - [ ] Creare `edit_company_profile` view in `apps/accounts/views.py` che:
    - Restituisca form pre-compilato con dati attuali del profilo
    - Aggiorni il profilo esistente in caso di POST valido
    - Redirect a `accounts:dashboard` dopo salvataggio
    - Limiti accesso a utenti autenticati con profilo esistente
- [ ] Task 2: Creare template per modifica profilo (AC: 1)
  - [ ] Creare `apps/accounts/templates/accounts/edit_profile.html` con form Bootstrap pre-compilato
  - [ ] Utilizzare lo stesso layout di `create_profile.html` ma con valori esistenti
- [ ] Task 3: Configurare URL routing per modifica (AC: 1)
  - [ ] Aggiungere path `profile/edit/` in `apps/accounts/urls.py`
  - [ ] Collegare alla view `edit_company_profile`
- [ ] Task 4: Aggiornare view di creazione per redirect se profilo esiste (AC: 1, 2)
  - [ ] Modificare `create_company_profile` view per reindirizzare a `edit_company_profile` se l'utente ha già un profilo
- [ ] Task 5: Test (AC: 1, 2)
  - [ ] Test modifica profilo con dati validi
  - [ ] Test validazione campi (come nella creazione)
  - [ ] Test accesso negato per utenti non autenticati
  - [ ] Test accesso negato per utenti senza profilo esistente
  - [ ] Test che dati aggiornati siano effettivamente salvati

## Dev Notes

### Architettura e vincoli
- **Modifica su modello esistente:** Il profilo è già stato creato in Story 1.4. La modifica deve usare lo stesso modello `CompanyProfile`.
- **Cifratura P.IVA:** Il campo `partita_iva` è cifrato con AES-256 (EncryptedCharField). La modifica deve mantenere la cifratura.
- **Associazione tenant:** Il profilo è associato al tenant dell'utente. La modifica non deve cambiare l'associazione.
- **Isolamento dati:** Ogni utente modifica solo il proprio profilo. Query deve filtrare per `user=request.user`.
- **Testing:** TDD obbligatorio. Testare modifica, validazione, cifratura, isolamento tenant.
- **Pattern esistenti:** Utilizzare lo stesso pattern di form e view della creazione.

### Riferimenti
- [Source: planning-artifacts/epics.md#Story 1.5: Modifica Profilo Aziendale]
- [Source: planning-artifacts/architecture.md#Django App Structure]
- [Source: planning-artifacts/prd.md#FR27, FR28]
- [Source: apps/accounts/models.py] (modello CompanyProfile)
- [Source: apps/accounts/forms.py] (CompanyProfileForm)
- [Source: apps/accounts/views.py] (create_company_profile per pattern)
- [Source: apps/accounts/urls.py] (pattern URL esistente)

### Contexto da Story 1.4
- **Pattern di form:** `CompanyProfileForm` già esistente con validazione P.IVA (11 cifre)
- **Crittografia:** `EncryptedCharField` per `partita_iva` con `FIELD_ENCRYPTION_KEY` in settings
- **View pattern:** Funzione-based view con `@login_required` e check esistenza profilo
- **Template pattern:** Bootstrap form in `create_profile.html`
- **URL pattern:** `path('profile/create/', ...)` con namespace `accounts`

### Struttura modifica
1. **Edit view:** simile a create ma con `instance=profilo_esistente` nel form
2. **Template:** riutilizzare struttura create, con valori pre-compilati
3. **URL:** `/profile/edit/` accanto a `/profile/create/`
4. **Redirect create:** se profilo esiste, redirect a edit invece che mostrare errore

## Dev Agent Record

### Agent Model Used

Amelia (bmad-dev) — BMAD Phase 4 Implementation

### Debug Log References

### Completion Notes List

### File List

- `apps/accounts/views.py` — Aggiunta edit_company_profile view
- `apps/accounts/urls.py` — Aggiunto path 'profile/edit/'
- `apps/accounts/templates/accounts/edit_profile.html` — Template modifica profilo
- `tests/test_story_1_5.py` — Test per modifica profilo
