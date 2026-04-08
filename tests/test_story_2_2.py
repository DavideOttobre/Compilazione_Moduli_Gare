# Story 2.2: Parsing PDF Nativo
# AC-1: Testo estratto correttamente da PDF nativo
# AC-2: Parsing < 2 minuti (NFR1)
# AC-3: Errore friendly in italiano su fallimento

import time
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.http import Http404

from apps.accounts.models import Tenant, CompanyProfile
from apps.document_parser.models import Document

User = get_user_model()


class PDFParserServiceTests(TestCase):
    """Test per extract_text_from_pdf service — Task 1"""

    def setUp(self):
        self.tenant = Tenant.objects.create(name='Test SRL')
        self.user = User.objects.create_user(
            email='test@test.com', password='TestPass123!', tenant=self.tenant
        )

    def test_service_exists(self):
        """AC-1: Service module esiste"""
        from apps.document_parser import services
        self.assertTrue(hasattr(services, 'extract_text_from_pdf'))

    @patch('apps.document_parser.services.pdfplumber')
    def test_extract_text_single_page(self, mock_pdfplumber):
        """AC-1: Estrazione testo da PDF singola pagina"""
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = 'Contenuto della pagina uno'
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf

        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='disciplinare.pdf',
            file_type='pdf',
            file_size=1024,
        )

        from apps.document_parser.services import extract_text_from_pdf
        result = extract_text_from_pdf(doc)
        self.assertEqual(result, 'Contenuto della pagina uno')

    @patch('apps.document_parser.services.pdfplumber')
    def test_extract_text_multi_page(self, mock_pdfplumber):
        """AC-1: Testo multi-pagina concatenato"""
        mock_pdf = MagicMock()
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = 'Pagina uno.'
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = 'Pagina due.'
        mock_pdf.pages = [mock_page1, mock_page2]
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf

        doc = Document.objects.create(
            user=self.user,
            file='documents/multipage.pdf',
            original_name='multipage.pdf',
            file_type='pdf',
            file_size=2048,
        )

        from apps.document_parser.services import extract_text_from_pdf
        result = extract_text_from_pdf(doc)
        self.assertEqual(result, 'Pagina uno. Pagina due.')

    @patch('apps.document_parser.services.pdfplumber')
    def test_extract_text_corrupted_pdf(self, mock_pdfplumber):
        """AC-3: Errore friendly su PDF corrotto"""
        from core.exceptions import DocumentParseError
        mock_pdfplumber.open.side_effect = Exception('corrupted file')

        doc = Document.objects.create(
            user=self.user,
            file='documents/corrotto.pdf',
            original_name='corrotto.pdf',
            file_type='pdf',
            file_size=512,
        )

        from apps.document_parser.services import extract_text_from_pdf
        with self.assertRaises(DocumentParseError):
            extract_text_from_pdf(doc)

    @patch('apps.document_parser.services.pdfplumber')
    def test_extract_text_duration_under_2min(self, mock_pdfplumber):
        """AC-2: Parsing < 2 minuti (NFR1)"""
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = 'Testo veloce'
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf

        doc = Document.objects.create(
            user=self.user,
            file='documents/veloce.pdf',
            original_name='veloce.pdf',
            file_type='pdf',
            file_size=1024,
        )

        from apps.document_parser.services import extract_text_from_pdf
        start = time.time()
        extract_text_from_pdf(doc)
        duration = time.time() - start
        self.assertLess(duration, 120, 'Parsing deve completare in < 2 minuti')


class DocumentModelParsedContentTests(TestCase):
    """Test per campo parsed_content nel modello — Task 3"""

    def setUp(self):
        self.tenant = Tenant.objects.create(name='Test SRL')
        self.user = User.objects.create_user(
            email='test@test.com', password='TestPass123!', tenant=self.tenant
        )

    def test_document_has_parsed_content_field(self):
        """AC-1: Campo parsed_content presente"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='test.pdf',
            file_type='pdf',
            file_size=1024,
            parsed_content='Testo estratto dal PDF',
        )
        doc.refresh_from_db()
        self.assertEqual(doc.parsed_content, 'Testo estratto dal PDF')

    def test_parsed_content_nullable(self):
        """AC-1: parsed_content nullable (default None)"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='test.pdf',
            file_type='pdf',
            file_size=1024,
        )
        self.assertIsNone(doc.parsed_content)


class ParseDocumentViewTests(TestCase):
    """Test per parse_document view — Task 2"""

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

    def _create_uploaded_pdf(self):
        """Helper: crea documento PDF con status uploaded"""
        return Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='disciplinare.pdf',
            file_type='pdf',
            file_size=1024,
            status='uploaded',
        )

    def test_parse_url_exists(self):
        """AC-1: URL documents/parse/<pk>/ esiste"""
        doc = self._create_uploaded_pdf()
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse/{doc.pk}/')
        self.assertNotEqual(response.status_code, 404)

    def test_parse_redirects_anonymous(self):
        """AC-1: Redirect per utenti non autenticati"""
        doc = self._create_uploaded_pdf()
        response = self.client.get(f'/documents/parse/{doc.pk}/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_parse_only_pdf_documents(self):
        """AC-1: Solo documenti PDF"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.docx',
            original_name='test.docx',
            file_type='docx',
            file_size=1024,
            status='uploaded',
        )
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse/{doc.pk}/')
        self.assertEqual(response.status_code, 400)

    def test_parse_only_uploaded_status(self):
        """AC-1: Solo documenti con status uploaded"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='test.pdf',
            file_type='pdf',
            file_size=1024,
            status='parsed',
        )
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse/{doc.pk}/')
        self.assertEqual(response.status_code, 400)

    @patch('apps.document_parser.views.extract_text_from_pdf')
    def test_parse_success_updates_status(self, mock_extract):
        """AC-1: Status aggiornato a 'parsed' dopo successo"""
        mock_extract.return_value = 'Testo estratto dal PDF'
        doc = self._create_uploaded_pdf()
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse/{doc.pk}/')
        doc.refresh_from_db()
        self.assertEqual(doc.status, 'parsed')

    @patch('apps.document_parser.views.extract_text_from_pdf')
    def test_parse_success_saves_content(self, mock_extract):
        """AC-1: Contenuto estratto salvato in parsed_content"""
        mock_extract.return_value = 'Testo estratto dal PDF'
        doc = self._create_uploaded_pdf()
        self.client.login(email='test@test.com', password='TestPass123!')
        self.client.get(f'/documents/parse/{doc.pk}/')
        doc.refresh_from_db()
        self.assertEqual(doc.parsed_content, 'Testo estratto dal PDF')

    @patch('apps.document_parser.views.extract_text_from_pdf')
    def test_parse_success_renders_result(self, mock_extract):
        """AC-1: Template risultato con anteprima contenuto"""
        mock_extract.return_value = 'Testo estratto dal PDF'
        doc = self._create_uploaded_pdf()
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse/{doc.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testo estratto dal PDF')

    @patch('apps.document_parser.views.extract_text_from_pdf')
    def test_parse_failure_updates_status_error(self, mock_extract):
        """AC-3: Status 'error' su fallimento parsing"""
        from core.exceptions import DocumentParseError
        mock_extract.side_effect = DocumentParseError(
            message='Impossibile leggere il documento. Verifica che il file sia un PDF valido.'
        )
        doc = self._create_uploaded_pdf()
        self.client.login(email='test@test.com', password='TestPass123!')
        self.client.get(f'/documents/parse/{doc.pk}/')
        doc.refresh_from_db()
        self.assertEqual(doc.status, 'error')

    @patch('apps.document_parser.views.extract_text_from_pdf')
    def test_parse_failure_shows_friendly_error(self, mock_extract):
        """AC-3: Messaggio errore friendly in italiano"""
        from core.exceptions import DocumentParseError
        mock_extract.side_effect = DocumentParseError(
            message='Impossibile leggere il documento. Verifica che il file sia un PDF valido.'
        )
        doc = self._create_uploaded_pdf()
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse/{doc.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Impossibile leggere')
        self.assertNotContains(response, 'Traceback')

    def test_parse_tenant_isolation(self):
        """AC-1: Isolamento tenant — solo propri documenti"""
        user2 = User.objects.create_user(
            email='other@test.com', password='TestPass123!', tenant=self.tenant
        )
        doc = self._create_uploaded_pdf()
        self.client.login(email='other@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse/{doc.pk}/')
        # Redirect a upload_document con messaggio errore
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/documents/upload/')

    def test_parse_nonexistent_document(self):
        """AC-1: Redirect per documento inesistente"""
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get('/documents/parse/99999/')
        # Redirect a upload_document con messaggio errore
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/documents/upload/')
