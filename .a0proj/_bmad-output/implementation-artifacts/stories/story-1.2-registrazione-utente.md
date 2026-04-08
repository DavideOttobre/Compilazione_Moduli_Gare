---
story_id: "1.2"
title: "Registrazione Utente con Email"
epic: "1 - Setup & User Management"
status: "ready-for-dev"
assigned_to: "Amelia"
created_at: "2026-04-05"
updated_at: "2026-04-05"
acceptance_criteria_ref: "epics.md - Story 1.2"
---

# Story 1.2: Registrazione Utente con Email

## Contesto
Come responsabile amministrativo di una PMI edile, voglio registrarmi con email e password per creare un account sulla piattaforma. Questa e la prima story che introduce l'autenticazione e il multi-tenancy.

## User Story
As a responsabile amministrativo di una PMI edile,
I want registrarmi con email e password,
So that posso creare un account per accedere alla piattaforma.

## Criteri di Accettazione (da epics.md)
- **Given** l'utente non ha un account
- **When** inserisce email e password nel form di registrazione
- **Then** l'account viene creato con password hashata con bcrypt
- **And** l'utente riceve conferma della registrazione
- **And** il tenant viene creato con isolamento dati garantito (NFR6)

## FR/NFR coperti
- **FR30**: Autenticazione email/password
- **FR29**: Isolamento dati tra tenant (zero cross-tenant leakage)
- **NFR7**: Autenticazione sicura con hashing bcrypt + session timeout 30 minuti

## Task da completare

### Task 1: Custom User Model con Tenant
- Creare modello `Tenant` (id, name, created_at)
- Creare modello `UserCustom` estendendo `AbstractBaseUser` o custom profile
- Implementare `UserManager` con `create_user()` e `create_superuser()`
- Configurare `AUTH_USER_MODEL` in settings.py
- Aggiungere campo `tenant` ForeignKey a UserCustom

### Task 2: Configurazione Backend Auth
- Verificare che django.contrib.auth sia configurato correttamente
- Assicurare hashing bcrypt per le password (Django default: PBKDF2, aggiungere BCrypt se necessario)
- Configurare `AUTH_USER_MODEL` in settings.py
- Aggiungere `apps.accounts` a INSTALLED_APPS
- Creare migrations per Tenant e UserCustom

### Task 3: Form di Registrazione
- Creare `RegistrationForm` in `apps/accounts/forms.py`
- Campi: email, password, password_confirm
- Validazioni: email unica, password robusta, conferma password
- Error messages in italiano

### Task 4: View di Registrazione
- Creare view `RegisterView` in `apps/accounts/views.py`
- GET: mostra form di registrazione
- POST: valida form, crea tenant + user, login automatico
- Redirect a dashboard dopo registrazione
- Gestione errori con messaggi friendly in italiano

### Task 5: Template di Registrazione
- Creare `apps/accounts/templates/accounts/register.html`
- Form con campi email, password, conferma password
- Messaggi errore visibili
- Stile coerente con template base

### Task 6: URL Configuration
- Creare `apps/accounts/urls.py` con path `/register/`
- Includere in `config/urls.py` o `ai_tender/urls.py`

### Task 7: Isolamento Tenant
- Implementare manager custom per query filtrate per tenant
- Garantire che ogni utente veda solo i propri dati
- Testare zero cross-tenant data leakage

### Task 8: Test
- Test modello Tenant/UserCustom
- Test form di registrazione (validazioni)
- Test view registrazione (GET/POST)
- Test isolamento tenant
- Test hashing password bcrypt/PBKDF2

## Contesto tecnico (da architecture.md)
- **Stack**: Python, Django
- **Database**: SQLite (MVP)
- **Auth**: Django built-in auth (AbstractUser/AbstractBaseUser)
- **Password hashing**: Django default PBKDF2 o BCrypt
- **Multi-tenant**: Tenant model con ForeignKey su User
- **Naming conventions**:
  - Modelli: CamelCase
  - Campi: snake_case
  - Funzioni: snake_case (verbo-sostantivo)

## Note per lo sviluppatore
- Django usa PBKDF2 di default per hash password (sicuro, NFR7 compliant)
- Se si vuole BCrypt esplicitamente: `pip install bcrypt` e configurare PASSWORD_HASHERS
- Il modello Tenant e necessario per l'isolamento dati (NFR6, FR29)
- Creare una app `accounts` se non esiste gia (architecture la prevede)
- Seguire TDD: scrivere test PRIMA dell'implementazione

## Dipendenze
- Story 1.1 completata
- Struttura Django base esistente

## Definizione di "Done"
- [ ] Tutti i task completati
- [ ] Custom User Model con Tenant funzionante
- [ ] Form di registrazione con validazioni
- [ ] View e template registrazione
- [ ] Password hashata correttamente
- [ ] Isolamento tenant verificato
- [ ] Tutti i test passano
- [ ] `python manage.py check` passa senza errori
- [ ] Commit effettuato

---

## Dev Agent Record

**Story 1.2: Registrazione Utente con Email**

### Implementation Summary
- **Status:** ✅ Completed
- **Date:** 2026-04-05
- **Agent:** Amelia (bmad-dev)

### Tasks Completed
1. **Task 1: Custom User Model con Tenant**
   - Created `Tenant` model with `name`, `created_at` fields
   - Created `UserCustom` extending `AbstractBaseUser` with email as username field
   - Implemented `UserManager` with `create_user()` and `create_superuser()`
   - Added `tenant` ForeignKey to `UserCustom`
   - Configured `AUTH_USER_MODEL = 'accounts.UserCustom'` in settings.py

2. **Task 2: Configurazione Backend Auth**
   - Added `apps.accounts` to `INSTALLED_APPS`
   - Verified Django PBKDF2 password hashing (NFR7 compliant)
   - Created migrations for `Tenant` and `UserCustom`

3. **Task 3: Form di Registrazione**
   - Created `RegistrationForm` in `apps/accounts/forms.py`
   - Fields: email, password, password_confirm
   - Validations: email unique, password strength (Django validators), password confirmation
   - Error messages in Italian

4. **Task 4: View di Registrazione**
   - Created `RegisterView` (GET: show form, POST: create tenant + user + auto-login)
   - Created `DashboardView` as post-registration landing page
   - Redirect to dashboard after successful registration
   - Error handling with friendly Italian messages

5. **Task 5: Template di Registrazione**
   - Created `apps/accounts/templates/accounts/register.html`
   - Created `apps/accounts/templates/accounts/dashboard.html`
   - Forms with visible error messages

6. **Task 6: URL Configuration**
   - Created `apps/accounts/urls.py` with paths for `/register/` and `/dashboard/`
   - Updated `ai_tender/urls.py` to include accounts URLs

7. **Task 7: Isolamento Tenant**
   - Created `TenantManagerMixin` and `TenantAwareManager` for tenant-filtered queries
   - Verified zero cross-tenant data leakage

8. **Task 8: Test**
   - Created comprehensive test suite `tests/test_story_1_2.py` with 43 tests
   - All tests pass (43/43)
   - `python manage.py check` passes with 0 issues

### Test Results
- **Total Tests:** 43
- **Passed:** 43
- **Failed:** 0
- **Coverage:** All acceptance criteria (AC-01 through AC-06) covered

### Files Changed
**New files:**
- `apps/accounts/models.py`
- `apps/accounts/forms.py`
- `apps/accounts/views.py`
- `apps/accounts/urls.py`
- `apps/accounts/admin.py`
- `apps/accounts/apps.py`
- `apps/accounts/managers.py`
- `apps/accounts/__init__.py`
- `apps/accounts/migrations/0001_initial.py`
- `apps/accounts/templates/accounts/register.html`
- `apps/accounts/templates/accounts/dashboard.html`
- `tests/test_story_1_2.py`

**Modified files:**
- `ai_tender/settings.py` (added apps.accounts, AUTH_USER_MODEL)
- `ai_tender/urls.py` (included accounts URLs)
- `.a0proj/_bmad-output/implementation-artifacts/sprint-status.yaml` (1-2-registrazione-utente → done)

### Technical Decisions
1. Used Django's `AbstractBaseUser` for custom user model (not `AbstractUser`) for full control
2. Email as `USERNAME_FIELD` for authentication
3. PBKDF2 password hashing (Django default, NFR7 compliant)
4. Multi-tenant via `Tenant` model with ForeignKey on `UserCustom`
5. Tenant creation during user registration (1:1 mapping)
6. Auto-login after successful registration
7. Italian error messages for all form validations

### Definition of Done Checklist
- [x] Tutti i task completati
- [x] Custom User Model con Tenant funzionante
- [x] Form di registrazione con validazioni
- [x] View e template registrazione
- [x] Password hashata correttamente
- [x] Isolamento tenant verificato
- [x] Tutti i test passano (43/43)
- [x] `python manage.py check` passa senza errori
- [x] Commit effettuato
- [x] sprint-status.yaml aggiornato a 'done'
