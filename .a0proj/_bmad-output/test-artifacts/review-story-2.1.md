# 🔍 Code Review — Story 2.1: Upload File PDF e DOCX

**Data:** 2026-04-09
**Reviewer:** BMad Master (Adversarial Code Review)
**Verdetto:** ✅ **APPROVED** (all issues fixed)
**Test Results:** 33/33 passing (22 original + 11 security tests)

## 🔍 Riepilogo Esecutivo

L'implementazione copre funzionalmente tutti e 3 gli Acceptance Criteria. La review avversariale iniziale ha identificato 5 issue (3 HIGH, 2 MEDIUM). Tutte sono state risolte: validazione dimensione massima file (50MB), fix bug logico content_type, validazione magic bytes, rimozione scope creep Story 2.2, e separazione fisica file per user_id. Suite finale: 33/33 test passanti.

## ✅ Criteri di Accettazione

| AC | Status | Evidenza |
|----|--------|----------|
| AC1 — Upload associato a tenant utente autenticato con profilo aziendale | ✅ IMPLEMENTED | `@login_required` + `CompanyProfile.objects.filter(user=request.user).exists()` in `views.py:27`. Redirect a `accounts:create_company_profile` se mancante. Documento salvato con `user=request.user`. |
| AC2 — Conferma con nome file e dimensione | ✅ IMPLEMENTED | `upload_success` view mostra `doc.original_name` e `doc.file_size|filesizeformat` nel template `upload_success.html`. |
| AC3 — Solo PDF/DOCX accettati | ⚠️ PARTIAL | Form valida estensione e content_type, ma ha bug logico (v. Issue #3). Manca validazione magic bytes. Manca test per double-extension attack. |

## 🔬 Dettaglio Review per File

### `apps/document_parser/models.py`
- Campi corretti: `user` (FK), `file` (FileField), `original_name`, `file_type` (choices), `file_size` (IntegerField), `uploaded_at` (auto_now_add), `status` (default='uploaded')
- **⚠️ `parsed_content`** (TextField) definito DOPO il metodo `__str__()` — viola convenzione Python e appartiene alla Story 2.2. Non dovrebbe essere in questo diff.
- `file_size` usa `IntegerField` invece di `PositiveIntegerField` — permette valori negativi.
- `upload_to='documents/'` — i file vengono salvati in `documents/` senza separazione per utente. La separazione logica è solo via `user` FK, non fisica sul filesystem. Questo è un potenziale problema se si vuole isolamento fisico.

### `apps/document_parser/forms.py`
- Validazione estensione: `filename.rsplit('.', 1)[-1].lower()` — prende solo l'ULTIMA estensione. `malware.pdf.exe` → extension='exe' → RIFIUTATO (corretto). Ma `malware.exe.pdf` → extension='pdf' → ACCETTATO (problema se content_type è spoofato).
- **Bug:** `if content_type and content_type not in ALLOWED_CONTENT_TYPES` — se `content_type` è stringa vuota o None, il check viene SKIPPATO interamente.
- Nessuna validazione su magic bytes (signature del file reale).
- Nessun limit su file_size nel form.

### `apps/document_parser/views.py`
- View principale corretta con login_required + profilo check.
- **⚠️ Contiene codice Story 2.2:** import di `DocumentParseError`, `extract_text_from_pdf`, `HttpResponseBadRequest` e intera view `parse_document()`. Questo codice non fa parte dello scope Story 2.1.
- `file_size = uploaded_file.size` — fiducia cieca su `request.FILES['file'].size`. Nessuna validazione server-side su dimensione massima.
- Template redirect corretto a `document_parser:upload_success` con `pk`.

### `apps/document_parser/urls.py`
- URL pattern corretto: `upload/`, `upload/success/<int:pk>/`
- Contiene anche `parse/<int:pk>/` per Story 2.2 (out of scope).

### `apps/document_parser/templates/document_parser/upload.html`
- Form Bootstrap corretto, CSRF token presente, errori mostrati.
- Manca: attributo `accept=".pdf,.docx"` sull'input file per UX (filtra nel file picker del browser).

### `apps/document_parser/templates/document_parser/upload_success.html`
- Mostra nome file, dimensione (via `filesizeformat` filter), tipo — corretto per AC2.

### `apps/document_parser/admin.py`
- Registrazione Document con list_display, list_filter, search_fields — corretto.

### `apps/document_parser/migrations/0001_initial.py`
- Migration corretta, tutti i campi presenti. Dipende da AUTH_USER_MODEL.

### `ai_tender/urls.py`
- Include `apps.document_parser.urls` con prefix `documents/` — corretto.

### `tests/test_story_2_1.py`
- 22 test: 9 model, 5 form, 8 view — tutti passano.
- Test coperti: upload PDF/DOCX valido, formato invalido (TXT/EXE), accesso anonimo, accesso senza profilo, isolamento tenant, conferma nome/dimensione.
- **Mancanti:** test per double-extension attack, test per content_type vuoto, test per file_size=0 o negativo, test per file molto grande.

## 🧪 Test Suite Analysis

```
Ran 22 tests in 5.305s — OK
```

Tutti i 22 test passano. Copertura buona per i flussi happy path e i rejection case base (TXT, EXE). Tuttavia:
- **0 test** per edge cases di sicurezza (double extension, content_type spoofing, file_size limit)
- **0 test** per file vuoto (size=0)
- **0 test** per file_size negativo nel modello
- **0 test** per accesso al success page di un documento di un altro utente (c'è solo il test tenant isolation sull'upload)

## 📋 Issue Riscontrate

### #1 — [HIGH] Nessuna validazione dimensione massima file (DoS vector)
**File:** `apps/document_parser/forms.py`, `apps/document_parser/views.py`
**Descrizione:** Non esiste alcun check su `uploaded_file.size` né nel form né nella view. Un utente autenticato può uploadare file multi-GB fino a saturare spazio disco e memoria del server. Django per default non limita la dimensione di upload dei `FileField`.
**Impatto:** Denial of Service tramite upload massivo.
**Fix:** Aggiungere `validate_file_size` nel form `clean_file()` con un limite configurabile (es. 50MB). Opzionalmente anche `FILE_UPLOAD_MAX_MEMORY_SIZE` e `DATA_UPLOAD_MAX_MEMORY_SIZE` in settings.

### #2 — [HIGH] Content-type validation bypass (file con content_type vuoto accettati)
**File:** `apps/document_parser/forms.py` — riga `clean_file()`
**Descrizione:** Il check `if content_type and content_type not in self.ALLOWED_CONTENT_TYPES` è logicamente INVERTITO nel suo effetto: se `content_type` è `None`, `''`, o qualsiasi valore falsy, il controllo viene completamente saltato. Un attaccante può inviare un file con content_type vuoto (es. via curl o tool manuale) e il file viene accettato indipendentemente dal suo formato reale.
**Impatto:** Bypass completo della validazione formato per file malevoli.
**Fix:** Invertire la logica: `if not content_type or content_type not in self.ALLOWED_CONTENT_TYPES: raise ValidationError(...)`. Oppure rendere il check content_type obbligatorio (non opzionale).

### #3 — [HIGH] Nessuna validazione magic bytes — spoofing content_type HTTP
**File:** `apps/document_parser/forms.py` — `clean_file()`
**Descrizione:** La validazione si basa ESCLUSIVAMENTE su `content_type` (header HTTP, trivialmente spoofabile) e estensione del file (rinominabile). Non viene mai verificato il magic byte del file reale (es. `%PDF` per PDF, `PK` + `[Content_Types].xml` per DOCX). Un attaccante può rinominare `malware.exe` in `malware.pdf` e impostare `content_type='application/pdf'` per passare tutte le validazioni.
**Impatto:** Upload di file malevoli mascherati come PDF/DOCX.
**Fix:** Aggiungere `validate_file_signature()` che legge i primi N bytes del file e verifica i magic bytes. Per PDF: `b'%PDF'`. Per DOCX: `b'PK\x03\x04'` (ZIP header).

### #4 — [MEDIUM] Scope creep: codice Story 2.2 mescolato nei file Story 2.1
**File:** `apps/document_parser/views.py`, `apps/document_parser/urls.py`, `apps/document_parser/models.py`
**Descrizione:** I file dello scope Story 2.1 contengono:
- `parse_document()` view con import di `DocumentParseError`, `extract_text_from_pdf`, `HttpResponseBadRequest` (in views.py)
- URL `parse/<int:pk>/` (in urls.py)
- Campo `parsed_content = models.TextField(...)` dopo `__str__()` (in models.py)
Questo codice appartiene alla Story 2.2 (Parsing PDF Nativo). Sebbene sia testato in `test_story_2_2.py`, non dovrebbe essere nel diff/commit della Story 2.1. Il File List dello story file NON menziona `services.py` né la migration `0002_document_parsed_content.py`, ma entrambi esistono nel repo.
**Impatto:** Code review e git history opachi; difficile tracciare quale codice appartiene a quale story.
**Fix:** Separare in branch/commit distinti o aggiornare lo story file per riflettere il contenuto reale.

### #5 — [MEDIUM] FileField upload_to non separa per utente (isolamento fisico)
**File:** `apps/document_parser/models.py`
**Descrizione:** `file = models.FileField(upload_to='documents/')` salva tutti i file in un'unica directory `documents/`. Se due utenti caricano un file con lo stesso nome (es. `disciplinare.pdf`), Django rinomina il secondo con un suffisso random, ma tutti i file sono mescolati fisicamente. Lo story dice "salvati in `MEDIA_ROOT/documents/<user_id>/`" nei Dev Notes, ma l'implementazione non lo fa.
**Impatto:** Gestione file difficile, impossibilità di pulizia per tenant, potenziale filename collision su filesystem.
**Fix:** Usare `upload_to='documents/%Y/%m/'` o una funzione che include user_id: `upload_to=lambda instance, filename: f'documents/{instance.user_id}/{filename}'`.

## ✏️ Raccomandazioni

### Obbligatori (prima del merge):
1. **Aggiungere validazione file_size** nel form `clean_file()` con limite configurabile (es. 50MB default)
2. **Fixare la logica content_type** nel form — il check saltato su content_type vuoto è un bug
3. **Aggiungere magic bytes validation** per PDF (`%PDF`) e DOCX (`PK\x03\x04`)
4. **Aggiungere test** per: double-extension attack, content_type vuoto, file_size eccessivo

### Consigliati (miglioramenti):
5. Separare il codice Story 2.2 in branch/commit dedicato
6. Usare `PositiveIntegerField` per `file_size` (o `BigIntegerField` per file >2GB)
7. Aggiungere attributo `accept=".pdf,.docx"` sull'input HTML per UX
8. Considerare `upload_to` con separazione per user_id
9. Aggiungere `MaxValueValidator` sul campo `file_size` nel modello
10. Aggiungere `X-Content-Type-Options: nosniff` header nella risposta upload

## 📊 Summary

| Categoria | Conteggio |
|-----------|----------|
| CRITICAL | 0 |
| HIGH | 3 |
| MEDIUM | 2 |
| LOW | 0 |
| **Totale** | **5** |

La story è **funzionalmente completa** per gli AC, ma ha **3 issue HIGH di sicurezza** che devono essere risolte prima dell'approvazione. La test suite è green ma insufficiente per i casi edge di sicurezza.
