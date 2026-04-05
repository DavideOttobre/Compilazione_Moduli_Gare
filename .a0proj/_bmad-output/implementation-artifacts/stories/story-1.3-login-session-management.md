---
story_id: "1.3"
title: "Login e Session Management"
epic: "1 - Autenticazione e Gestione Profilo Aziendale"
status: "ready-for-dev"
assigned_to: "Amelia"
created_at: "2026-04-05"
updated_at: "2026-04-05"
acceptance_criteria_ref: "epics.md - Story 1.3"
---

# Story 1.3: Login e Session Management

## Contesto
Come utente registrato, voglio accedere con le mie credenziali per utilizzare la piattaforma in modo sicuro. Questa story introduce il login e la gestione delle sessioni, costruendo sul modello utente custom creato in Story 1.2.

## User Story
As a utente registrato,
I want accedere con le mie credenziali,
So that posso utilizzare la piattaforma in modo sicuro.

## Criteri di Accettazione (da epics.md)
- **Given** l'utente ha un account attivo
- **When** inserisce email e password valide
- **Then** la sessione viene creata con timeout di 30 minuti (NFR7)
- **And** i dati sono protetti in transit con TLS 1.2+ (NFR5)
- **And** l'utente è reindirizzato alla dashboard

## FR/NFR coperti
- **FR30**: Autenticazione email/password (login)
- **NFR7**: Autenticazione sicura con hashing bcrypt + session timeout 30 minuti
- **NFR5**: Dazi protetti in transit con TLS 1.2+

## Task da completare

### Task 1: Login View e Form
- Creare `LoginForm` in `apps/accounts/forms.py` con campi email e password
- Creare `LoginView` in `apps/accounts/views.py` (GET: mostra form, POST: autentica e crea sessione)
- Validare credenziali con `authenticate()` di Django
- Gestione errori con messaggi friendly in italiano

### Task 2: Logout View
- Creare `LogoutView` in `apps/accounts/views.py`
- Invalidare la sessione corrente
- Redirect alla pagina di login dopo logout

### Task 3: Configurazione Session Timeout
- Configurare `SESSION_COOKIE_AGE = 1800` (30 minuti) in `settings.py`
- Configurare `SESSION_EXPIRE_AT_BROWSER_CLOSE = True`
- Assicurare che le sessioni siano salvate nel database

### Task 4: Template di Login
- Creare `apps/accounts/templates/accounts/login.html`
- Form con campi email e password
- Link per registrazione se non si ha account
- Messaggi errore visibili

### Task 5: URL Configuration
- Aggiungere path per `/login/` e `/logout/` in `apps/accounts/urls.py`

### Task 6: Middleware e Protezione
- Configurare `@login_required` per la view della dashboard
- Redirect a login per utenti non autenticati
- Mantenere la sessione attiva con richieste valide

### Task 7: Test
- Test login view (GET/POST con credenziali valide/non valide)
- Test logout view
- Test session timeout (mock del tempo)
- Test protezione dashboard (redirect a login se non autenticato)
- Test messaggi errore in italiano

## Contesto tecnico (da architecture.md + previous story)
- **Stack**: Python, Django
- **Database**: SQLite (MVP)
- **Auth**: Django built-in auth (già configurato in Story 1.2 con `AUTH_USER_MODEL`)
- **Session**: Django session framework (database-backed)
- **TLS**: Configurazione a livello di deployment (non codice, ma verificare settings)
- **Naming conventions**:
  - Modelli: CamelCase
  - Campi: snake_case
  - Funzioni: snake_case (verbo-sostantivo)

## Note per lo sviluppatore
- Django ha già un sistema di login/logout built-in, ma creiamo view custom per controllo completo
- Usare `authenticate()` e `login()` di `django.contrib.auth`
- Il timeout sessione è già configurato in Django con `SESSION_COOKIE_AGE`
- TLS è un requisito di deployment: verificare che il server sia configurato per HTTPS
- **Learnings da Story 1.2**:
  - Il modello `UserCustom` usa email come `USERNAME_FIELD`
  - Il manager `TenantAwareManager` è disponibile per query filtrate per tenant
  - Testare con il test runner esistente (`python manage.py test`)
  - Seguire TDD: scrivere test PRIMA dell'implementazione

## Dipendenze
- Story 1.2 completata (modello UserCustom, Tenant, registrazione)
- Struttura Django base esistente
- App `accounts` già creata

## Definizione di "Done"
- [ ] Tutti i task completati
- [ ] Form di login con validazione credenziali
- [ ] View di login/logout funzionanti
- [ ] Session timeout configurato a 30 minuti
- [ ] Template di login coerente con il design
- [ ] Protezione dashboard (login_required)
- [ ] Tutti i test passano
- [ ] `python manage.py check` passa senza errori
- [ ] Commit effettuato

---

## Dev Agent Record

**Story 1.3: Login e Session Management**

### Implementation Summary
- **Status:** 🔄 To be implemented
- **Date:** -
- **Agent:** Amelia (bmad-dev)

### Tasks Completed
- None yet

### Test Results
- **Total Tests:** -
- **Passed:** -
- **Failed:** -

### Files Changed
- None yet

### Technical Decisions
- TBD

---

## References
- [Source: epics.md#Story-1.3]
- [Source: architecture.md#Authentication]
- [Source: story-1.2-registrazione-utente.md#Dev-Agent-Record]

---

## Implementation Summary
- **Status:** ✅ Done
- **Date:** 2026-04-05
- **Agent:** Amelia (bmad-dev)

### Tasks Completed
- Task 1: LoginForm con campi email/password + LoginView (GET/POST)
- Task 2: LogoutView con invalidazione sessione
- Task 3: SESSION_COOKIE_AGE=1800, SESSION_EXPIRE_AT_BROWSER_CLOSE=True
- Task 4: Template login.html con form e link a registrazione
- Task 5: URL /login/ e /logout/ configurati in accounts/urls.py
- Task 6: DashboardView protetta con LoginRequiredMixin
- Task 7: 25 test completi TDD

### Test Results
- **Total Tests:** 25
- **Passed:** 25
- **Failed:** 0

### Files Changed
- apps/accounts/forms.py (+LoginForm)
- apps/accounts/views.py (+LoginView, +LogoutView, DashboardView→LoginRequiredMixin)
- apps/accounts/urls.py (added /login/, /logout/)
- apps/accounts/templates/accounts/login.html (new)
- ai_tender/settings.py (+session config)
- tests/test_story_1_3.py (new, 25 tests)
