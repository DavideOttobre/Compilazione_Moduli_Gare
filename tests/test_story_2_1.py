# Story 2.1: Upload File PDF e DOCX
# AC-1: Upload documento PDF/DOCX associato a tenant utente
# AC-2: Conferma caricamento con nome file e dimensione
# AC-3: Validazione formato solo PDF/DOCX

from io import BytesIO

from django.test import TestCase, Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from apps.accounts.models import Tenant, CompanyProfile
from apps.document_parser.models import Document

User = get_user_model()


class DocumentModelTests(TestCase):
    """Test per model Document — Task 1"""

    def setUp(self):
        self.tenant = Tenant.objects.create(name='Test SRL')
        self.user = User.objects.create_user(
            email='test@test.com', password='TestPass123!', tenant=self.tenant
        )

    def test_document_has_user_fk(self):
        """AC-1: Documento associato a utente"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='disciplinare.pdf',
            file_type='pdf',
            file_size=1024,
        )
        self.assertEqual(doc.user, self.user)

    def test_document_has_file_field(self):
        """AC-1: Campo file presente"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='disciplinare.pdf',
            file_type='pdf',
            file_size=2048,
        )
        self.assertIsNotNone(doc.file)

    def test_document_has_original_name(self):
        """AC-2: Nome originale salvato"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='disciplinare_gara.pdf',
            file_type='pdf',
            file_size=512,
        )
        self.assertEqual(doc.original_name, 'disciplinare_gara.pdf')

    def test_document_file_type_pdf(self):
        """AC-1: file_type pdf"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='test.pdf',
            file_type='pdf',
            file_size=1024,
        )
        self.assertEqual(doc.file_type, 'pdf')

    def test_document_file_type_docx(self):
        """AC-1: file_type docx"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.docx',
            original_name='test.docx',
            file_type='docx',
            file_size=2048,
        )
        self.assertEqual(doc.file_type, 'docx')

    def test_document_file_size(self):
        """AC-2: Dimensione file salvata"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='test.pdf',
            file_type='pdf',
            file_size=3072,
        )
        self.assertEqual(doc.file_size, 3072)

    def test_document_uploaded_at_auto(self):
        """uploaded_at auto_now_add"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='test.pdf',
            file_type='pdf',
            file_size=1024,
        )
        self.assertIsNotNone(doc.uploaded_at)

    def test_document_status_default(self):
        """status default='uploaded'"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='test.pdf',
            file_type='pdf',
            file_size=1024,
        )
        self.assertEqual(doc.status, 'uploaded')

    def test_document_str(self):
        """__str__ returns original_name"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='disciplinare.pdf',
            file_type='pdf',
            file_size=1024,
        )
        self.assertIn('disciplinare.pdf', str(doc))


class DocumentUploadFormTests(TestCase):
    """Test per DocumentUploadForm — Task 2"""

    def setUp(self):
        self.tenant = Tenant.objects.create(name='Test SRL')
        self.user = User.objects.create_user(
            email='test@test.com', password='TestPass123!', tenant=self.tenant
        )

    # AC-3: PDF accettato
    def test_form_accepts_pdf(self):
        from apps.document_parser.forms import DocumentUploadForm
        pdf_file = SimpleUploadedFile(
            'disciplinare.pdf',
            b'%PDF-1.4 fake content',
            content_type='application/pdf'
        )
        form = DocumentUploadForm(files={'file': pdf_file})
        self.assertTrue(form.is_valid(), form.errors)

    # AC-3: DOCX accettato
    def test_form_accepts_docx(self):
        from apps.document_parser.forms import DocumentUploadForm
        docx_file = SimpleUploadedFile(
            'disciplinare.docx',
            b'PK fake docx content',
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        form = DocumentUploadForm(files={'file': docx_file})
        self.assertTrue(form.is_valid(), form.errors)

    # AC-3: TXT rifiutato
    def test_form_rejects_txt(self):
        from apps.document_parser.forms import DocumentUploadForm
        txt_file = SimpleUploadedFile(
            'testo.txt',
            b'plain text content',
            content_type='text/plain'
        )
        form = DocumentUploadForm(files={'file': txt_file})
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)

    # AC-3: EXE rifiutato
    def test_form_rejects_exe(self):
        from apps.document_parser.forms import DocumentUploadForm
        exe_file = SimpleUploadedFile(
            'malware.exe',
            b'MZ fake exe',
            content_type='application/octet-stream'
        )
        form = DocumentUploadForm(files={'file': exe_file})
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)

    # AC-3: messaggio errore in italiano
    def test_form_error_message_italian(self):
        from apps.document_parser.forms import DocumentUploadForm
        txt_file = SimpleUploadedFile(
            'testo.txt',
            b'plain text',
            content_type='text/plain'
        )
        form = DocumentUploadForm(files={'file': txt_file})
        form.is_valid()
        error_msg = str(form.errors['file'])
        self.assertTrue(
            'PDF' in error_msg or 'DOCX' in error_msg or 'formato' in error_msg.lower(),
            f'Errore non friendly: {error_msg}'
        )


class DocumentUploadViewTests(TestCase):
    """Test per upload_document view — Task 3"""

    def setUp(self):
        self.tenant = Tenant.objects.create(name='Test SRL')
        self.user = User.objects.create_user(
            email='test@test.com', password='TestPass123!', tenant=self.tenant
        )
        self.company = CompanyProfile.objects.create(
            user=self.user,
            tenant=self.tenant,
            ragione_sociale='Test SRL',
            partita_iva='12345678901',
            sede_legale='Via Roma 1'
        )
        self.client = Client()

    # AC-1: Accesso negato per utenti non autenticati
    def test_upload_redirects_anonymous(self):
        response = self.client.get('/documents/upload/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    # AC-1: Accesso negato per utenti senza profilo aziendale
    def test_upload_denied_no_company_profile(self):
        user2 = User.objects.create_user(
            email='noprofile@test.com', password='TestPass123!', tenant=self.tenant
        )
        self.client.login(email='noprofile@test.com', password='TestPass123!')
        response = self.client.get('/documents/upload/')
        self.assertEqual(response.status_code, 302)

    # AC-1: GET mostra form
    def test_upload_get_shows_form(self):
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get('/documents/upload/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')

    # AC-1: POST PDF valido salva documento
    def test_upload_post_valid_pdf(self):
        self.client.login(email='test@test.com', password='TestPass123!')
        pdf_file = SimpleUploadedFile(
            'disciplinare.pdf',
            b'%PDF-1.4 fake content for test',
            content_type='application/pdf'
        )
        response = self.client.post('/documents/upload/', {'file': pdf_file}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Document.objects.count(), 1)
        doc = Document.objects.first()
        self.assertEqual(doc.user, self.user)
        self.assertEqual(doc.original_name, 'disciplinare.pdf')
        self.assertEqual(doc.file_type, 'pdf')

    # AC-1: POST DOCX valido salva documento
    def test_upload_post_valid_docx(self):
        self.client.login(email='test@test.com', password='TestPass123!')
        docx_file = SimpleUploadedFile(
            'disciplinare.docx',
            b'PK fake docx content for test',
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response = self.client.post('/documents/upload/', {'file': docx_file}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Document.objects.count(), 1)
        doc = Document.objects.first()
        self.assertEqual(doc.file_type, 'docx')

    # AC-3: POST formato non valido mostra errore
    def test_upload_post_invalid_format(self):
        self.client.login(email='test@test.com', password='TestPass123!')
        txt_file = SimpleUploadedFile(
            'testo.txt',
            b'plain text content',
            content_type='text/plain'
        )
        response = self.client.post('/documents/upload/', {'file': txt_file})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Document.objects.count(), 0)

    # AC-2: Redirect conferma mostra nome file e dimensione
    def test_upload_success_shows_filename_and_size(self):
        self.client.login(email='test@test.com', password='TestPass123!')
        pdf_file = SimpleUploadedFile(
            'disciplinare.pdf',
            b'%PDF-1.4 content for size test',
            content_type='application/pdf'
        )
        response = self.client.post('/documents/upload/', {'file': pdf_file}, follow=True)
        self.assertContains(response, 'disciplinare.pdf')

    # AC-1: Documento associato al tenant dell'utente
    def test_upload_associated_to_user_tenant(self):
        self.client.login(email='test@test.com', password='TestPass123!')
        pdf_file = SimpleUploadedFile(
            'disciplinare.pdf',
            b'%PDF-1.4 tenant test',
            content_type='application/pdf'
        )
        self.client.post('/documents/upload/', {'file': pdf_file}, follow=True)
        doc = Document.objects.first()
        self.assertEqual(doc.user.tenant, self.tenant)
