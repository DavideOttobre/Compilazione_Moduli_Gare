# Code Review Report — Story 2.1: Upload File PDF e DOCX

| Field | Value |
|---|---|
| **Story** | 2.1 — Upload File PDF e DOCX |
| **Epic** | 2 — Upload e Analisi Disciplinare di Gara |
| **Reviewer** | Amelia (bmad-dev) |
| **Date** | 2026-04-08 |
| **Verdict** | ✅ **APPROVED** |

---

## 1. Test Execution Summary

| Metric | Result |
|---|---|
| **Tests Found** | 22 |
| **Tests Passed** | 22 |
| **Tests Failed** | 0 |
| **Django Check** | 0 issues (0 silenced) |
| **Status** | ✅ **OK** |

```
Ran 22 tests in 5.222s
OK
```

### Test Breakdown

| Class | Tests | Status |
|---|---|---|
| `DocumentModelTests` | 9 | ✅ All pass |
| `DocumentUploadFormTests` | 5 | ✅ All pass |
| `DocumentUploadViewTests` | 8 | ✅ All pass |

---

## 2. Acceptance Criteria Verification

### AC-1: Documento associato a tenant utente

**Status: ✅ PASS**

| Check | Evidence |
|---|---|
| Document has `user` ForeignKey | `models.py:36` — `user = models.ForeignKey(settings.AUTH_USER_MODEL, ...)` |
| Document associated to tenant user | `test_upload_associated_to_user_tenant` — verifies `doc.user.tenant == self.tenant` |
| Access denied for anonymous users | `test_upload_redirects_anonymous` — 302 redirect to login |
| Access denied without CompanyProfile | `test_upload_denied_no_company_profile` — 302 redirect |
| File saved with user association | `test_upload_post_valid_pdf` — `doc.user == self.user` |

### AC-2: Conferma caricamento con nome file e dimensione

**Status: ✅ PASS**

| Check | Evidence |
|---|---|
| `original_name` field present | `models.py:39` — `original_name = models.CharField(max_length=255)` |
| `file_size` field present | `models.py:41` — `file_size = models.IntegerField()` |
| Success page shows filename | `test_upload_success_shows_filename_and_size` — `assertContains(response, 'disciplinare.pdf')` |
| Template displays metadata | `upload_success.html` — `{{ file_name }}`, `{{ file_size|filesizeformat }}` |

### AC-3: Validazione formato solo PDF/DOCX

**Status: ✅ PASS**

| Check | Evidence |
|---|---|
| PDF accepted | `test_form_accepts_pdf` — form valid |
| DOCX accepted | `test_form_accepts_docx` — form valid |
| TXT rejected | `test_form_rejects_txt` — form invalid |
| EXE rejected | `test_form_rejects_exe` — form invalid |
| Italian error messages | `test_form_error_message_italian` — error contains 'PDF' or 'DOCX' or 'formato' |
| Extension validation | `forms.py:38` — `extension not in self.ALLOWED_EXTENSIONS` |
| Content-type validation | `forms.py:45` — `content_type not in self.ALLOWED_CONTENT_TYPES` |

---

## 3. Code Quality Assessment

### 3.1 Model (`apps/document_parser/models.py`)

| Aspect | Rating | Notes |
|---|---|---|
| Field design | ✅ Good | All required fields present with correct types |
| Choices | ✅ Good | `FILE_TYPE_CHOICES` and `STATUS_CHOICES` well-defined |
| Meta options | ✅ Good | `verbose_name`, `ordering` configured |
| AC traceability | ✅ Excellent | Inline comments reference AC-1, AC-2, AC-3 |
| Docstring | ✅ Good | Lists satisfied ACs |

### 3.2 Form (`apps/document_parser/forms.py`)

| Aspect | Rating | Notes |
|---|---|---|
| Validation logic | ✅ Good | Extension + content_type dual validation |
| Error messages | ✅ Good | Italian messages for all error cases |
| Edge case handling | ✅ Good | Handles missing extension (empty string check) |
| AC traceability | ✅ Excellent | Inline comments for AC-1, AC-3 |

### 3.3 Views (`apps/document_parser/views.py`)

| Aspect | Rating | Notes |
|---|---|---|
| Authentication | ✅ Good | `@login_required` decorator with login_url |
| Profile gating | ✅ Good | CompanyProfile check before upload |
| Tenant isolation | ✅ Good | `upload_success` filters by `user=request.user` |
| Error handling | ✅ Good | DoesNotExist caught with user-friendly redirect |
| AC traceability | ✅ Excellent | Inline comments for AC-1, AC-2, AC-3 |

### 3.4 Templates

| Aspect | Rating | Notes |
|---|---|---|
| Upload form | ✅ Good | Bootstrap card layout, error display, help text |
| Success page | ✅ Good | Shows file_name, file_size (formatted), file_type |
| Navigation | ✅ Good | Links to dashboard and re-upload |
| Consistency | ✅ Good | Extends `base.html` with Bootstrap |

### 3.5 URL Routing

| Aspect | Rating | Notes |
|---|---|---|
| Namespace | ✅ Good | `app_name = 'document_parser'` |
| Paths | ✅ Good | `/documents/upload/` and `/documents/upload/success/<pk>/` |
| Integration | ✅ Good | Included in `ai_tender/urls.py` |

### 3.6 Admin (`apps/document_parser/admin.py`)

| Aspect | Rating | Notes |
|---|---|---|
| Registration | ✅ Good | `Document` registered with `@admin.register` |
| List display | ✅ Good | Shows `original_name`, `file_type`, `file_size`, `user`, `status`, `uploaded_at` |
| Filters | ✅ Good | `file_type`, `status`, `uploaded_at` |
| Search | ✅ Good | `original_name` searchable |

### 3.7 Tests (`tests/test_story_2_1.py`)

| Aspect | Rating | Notes |
|---|---|---|
| Coverage | ✅ Excellent | All 3 ACs covered by multiple tests |
| AC traceability | ✅ Excellent | Docstrings reference specific ACs |
| Setup | ✅ Good | Proper Tenant/User/CompanyProfile creation |
| Edge cases | ✅ Good | Invalid formats, anonymous access, missing profile |
| Tenant isolation | ✅ Good | Separate test verifies tenant association |

---

## 4. Issues Found

### Critical: 0

### Minor: 0

### Observations (non-blocking):

1. **`file_size` uses `IntegerField`**: Current implementation uses `IntegerField` which limits file size to ~2GB. For this use case (tender documents typically < 50MB), this is acceptable. Consider `BigIntegerField` for future scaling.

2. **Extension extracted from filename only**: The form validates both extension AND content_type, but the model stores `file_type` derived only from the extension. The dual validation in the form mitigates spoofing risk.

3. **MEDIA_ROOT paths**: Test artifacts suggest files are stored in both `media/documents/` and `documents/` at project root. Verify `MEDIA_ROOT` configuration is consistent.

---

## 5. AC Traceability Matrix

| AC | Description | Model | Form | View | Tests |
|---|---|---|---|---|---|
| AC-1 | Upload associato a tenant | `user` FK, `file` Field | — | CompanyProfile check, tenant filter | `test_document_has_user_fk`, `test_upload_associated_to_user_tenant`, `test_upload_redirects_anonymous`, `test_upload_denied_no_company_profile` |
| AC-2 | Conferma con nome e dimensione | `original_name`, `file_size` | — | Context in `upload_success` | `test_document_has_original_name`, `test_document_file_size`, `test_upload_success_shows_filename_and_size` |
| AC-3 | Solo PDF/DOCX accettati | `file_type` choices | Extension + content_type validation | Format validation via form | `test_form_accepts_pdf`, `test_form_accepts_docx`, `test_form_rejects_txt`, `test_form_rejects_exe`, `test_upload_post_invalid_format` |

---

## 6. Recommendation

| # | Recommendation | Priority |
|---|---|---|
| 1 | Consider `BigIntegerField` for `file_size` if large file support needed in future | Low |
| 2 | Verify `MEDIA_ROOT` configuration consistency | Low |
| 3 | Consider adding file size limit validation (max upload size) in form | Medium |

---

## 7. Final Verdict

| Criterion | Status |
|---|---|
| All tests passing (22/22) | ✅ |
| Django check 0 issues | ✅ |
| AC-1 fully covered | ✅ |
| AC-2 fully covered | ✅ |
| AC-3 fully covered | ✅ |
| AC traceability in code | ✅ |
| Code quality acceptable | ✅ |
| No critical issues | ✅ |

### ✅ **APPROVED — Ready for Done**

---

*Report generated by Amelia (bmad-dev) — 2026-04-08*
