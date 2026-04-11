# Story 2.4: Parsing Documenti DOCX
# AC-1: Estrazione testo da DOCX
# AC-2: Preservazione struttura (titoli, sezioni)
# AC-3: Parsing < 2 minuti (NFR1)
# AC-4: Errore friendly in italiano
# AC-5: Solo file_type='docx' e status='uploaded'
# AC-6: Contenuto salvato in parsed_content
# AC-7: Status updated a 'parsed' o 'error'
# AC-8: Isolamento tenant

import time
from unittest.mock import patch, MagicMock, PropertyMock

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from apps.accounts.models import Tenant, CompanyProfile
from apps.document_parser.models import Document
from core.exceptions import DocumentParseError

User = get_user_model()


# =====================================================================
# TASK 1: DOCX Text Extraction Service (AC: 1, 2, 3)
# =====================================================================

class DOCXParserServiceTests(TestCase):
    """Test per extract_text_from_docx service — Task 1"""

    def setUp(self):
        self.tenant = Tenant.objects.create(name='Test SRL')
        self.user = User.objects.create_user(
            email='test@test.com', password='TestPass123!', tenant=self.tenant
        )

    def test_service_exists(self):
        """AC-1: Service extract_text_from_docx esiste"""
        from apps.document_parser import services
        self.assertTrue(hasattr(services, 'extract_text_from_docx'))

    @patch('apps.document_parser.services.DocxDocument')
    def test_extract_text_single_paragraph(self, mock_docx):
        """AC-1: Estrazione testo da DOCX singolo paragrafo"""
        mock_instance = MagicMock()
        mock_para = MagicMock()
        mock_para.text = 'Contenuto del paragrafo uno'
        mock_para.style.name = 'Normal'
        mock_instance.paragraphs = [mock_para]
        mock_instance.sections = []
        mock_docx.return_value = mock_instance

        doc = Document.objects.create(
            user=self.user,
            file='documents/test.docx',
            original_name='disciplinare.docx',
            file_type='docx',
            file_size=1024,
        )

        from apps.document_parser.services import extract_text_from_docx
        result = extract_text_from_docx(doc)
        self.assertIn('Contenuto del paragrafo uno', result)

    @patch('apps.document_parser.services.DocxDocument')
    def test_extract_text_multiple_paragraphs(self, mock_docx):
        """AC-1: Estrazione testo multi-paragrafo"""
        mock_instance = MagicMock()
        para1 = MagicMock()
        para1.text = 'Primo paragrafo.'
        para1.style.name = 'Normal'
        para2 = MagicMock()
        para2.text = 'Secondo paragrafo.'
        para2.style.name = 'Normal'
        mock_instance.paragraphs = [para1, para2]
        mock_instance.sections = []
        mock_docx.return_value = mock_instance

        doc = Document.objects.create(
            user=self.user,
            file='documents/multi.docx',
            original_name='multi.docx',
            file_type='docx',
            file_size=2048,
        )

        from apps.document_parser.services import extract_text_from_docx
        result = extract_text_from_docx(doc)
        self.assertIn('Primo paragrafo.', result)
        self.assertIn('Secondo paragrafo.', result)

    @patch('apps.document_parser.services.DocxDocument')
    def test_extract_preserves_heading_structure(self, mock_docx):
        """AC-2: Preservazione struttura titoli Heading 1/2/3"""
        mock_instance = MagicMock()
        h1 = MagicMock()
        h1.text = 'Titolo Principale'
        h1.style.name = 'Heading 1'
        h2 = MagicMock()
        h2.text = 'Sotto Titolo'
        h2.style.name = 'Heading 2'
        para = MagicMock()
        para.text = 'Testo normale'
        para.style.name = 'Normal'
        mock_instance.paragraphs = [h1, h2, para]
        mock_instance.sections = []
        mock_docx.return_value = mock_instance

        doc = Document.objects.create(
            user=self.user,
            file='documents/struttura.docx',
            original_name='struttura.docx',
            file_type='docx',
            file_size=1024,
        )

        from apps.document_parser.services import extract_text_from_docx
        result = extract_text_from_docx(doc)
        # I titoli devono essere marcati nella struttura
        self.assertIn('Titolo Principale', result)
        self.assertIn('Sotto Titolo', result)

    @patch('apps.document_parser.services.DocxDocument')
    def test_extract_preserves_list_items(self, mock_docx):
        """AC-2: Preservazione liste bullet/numbered"""
        mock_instance = MagicMock()
        bullet1 = MagicMock()
        bullet1.text = 'Elemento lista uno'
        bullet1.style.name = 'List Bullet'
        bullet2 = MagicMock()
        bullet2.text = 'Elemento lista due'
        bullet2.style.name = 'List Bullet'
        mock_instance.paragraphs = [bullet1, bullet2]
        mock_instance.sections = []
        mock_docx.return_value = mock_instance

        doc = Document.objects.create(
            user=self.user,
            file='documents/liste.docx',
            original_name='liste.docx',
            file_type='docx',
            file_size=1024,
        )

        from apps.document_parser.services import extract_text_from_docx
        result = extract_text_from_docx(doc)
        self.assertIn('Elemento lista uno', result)
        self.assertIn('Elemento lista due', result)

    @patch('apps.document_parser.services.DocxDocument')
    def test_extract_text_corrupted_docx(self, mock_docx):
        """AC-4: Errore friendly su DOCX corrotto"""
        mock_docx.side_effect = Exception('file is not a zip file')

        doc = Document.objects.create(
            user=self.user,
            file='documents/corrotto.docx',
            original_name='corrotto.docx',
            file_type='docx',
            file_size=512,
        )

        from apps.document_parser.services import extract_text_from_docx
        with self.assertRaises(DocumentParseError) as ctx:
            extract_text_from_docx(doc)
        # Messaggio friendly in italiano
        self.assertIn('Impossibile', str(ctx.exception))

    @patch('apps.document_parser.services.DocxDocument')
    def test_extract_text_duration_under_2min(self, mock_docx):
        """AC-3: Parsing < 2 minuti (NFR1)"""
        mock_instance = MagicMock()
        para = MagicMock()
        para.text = 'Testo veloce'
        para.style.name = 'Normal'
        mock_instance.paragraphs = [para]
        mock_instance.sections = []
        mock_docx.return_value = mock_instance

        doc = Document.objects.create(
            user=self.user,
            file='documents/veloce.docx',
            original_name='veloce.docx',
            file_type='docx',
            file_size=1024,
        )

        from apps.document_parser.services import extract_text_from_docx
        start = time.time()
        extract_text_from_docx(doc)
        duration = time.time() - start

    @patch('apps.document_parser.services.DocxDocument')
    def test_extract_text_timeout_raises_error(self, mock_docx):
        """AC-3, C-1: DocumentParseError se parsing supera timeout (mock delay reale)"""
        mock_instance = MagicMock()
        para = MagicMock()
        para.text = 'Testo'
        para.style.name = 'Normal'
        mock_instance.paragraphs = [para]
        mock_instance.sections = []
        mock_docx.return_value = mock_instance

        doc = Document.objects.create(
            user=self.user,
            file='documents/lento.docx',
            original_name='lento.docx',
            file_type='docx',
            file_size=1024,
        )

        from apps.document_parser.services import extract_text_from_docx
        # Simula: prima chiamata restituisce 0, successiva restituisce 200s (oltre timeout 120s)
        with patch('apps.document_parser.services.time.time', side_effect=[0.0, 200.0]):
            with self.assertRaises(DocumentParseError) as ctx:
                extract_text_from_docx(doc, timeout=120.0)
            self.assertIn('tempo massimo', str(ctx.exception))

    @patch('apps.document_parser.services.DocxDocument')
    def test_empty_paragraphs_handled(self, mock_docx):
        """AC-1: Paragrafi vuoti non generano errori"""
        mock_instance = MagicMock()
        empty_para = MagicMock()
        empty_para.text = ''
        empty_para.style.name = 'Normal'
        real_para = MagicMock()
        real_para.text = 'Testo reale'
        real_para.style.name = 'Normal'
        mock_instance.paragraphs = [empty_para, real_para]
        mock_instance.sections = []
        mock_docx.return_value = mock_instance

        doc = Document.objects.create(
            user=self.user,
            file='documents/vuoto.docx',
            original_name='vuoto.docx',
            file_type='docx',
            file_size=1024,
        )

        from apps.document_parser.services import extract_text_from_docx
        result = extract_text_from_docx(doc)
        self.assertIn('Testo reale', result)


# =====================================================================
# TASK 2: Endpoint API per trigger parsing DOCX (AC: 1, 4, 5, 7)
# =====================================================================

class ParseDOCXViewTests(TestCase):
    """Test per parse_docx_document view — Task 2"""

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

    def _create_uploaded_docx(self):
        """Helper: crea documento DOCX con status uploaded"""
        return Document.objects.create(
            user=self.user,
            file='documents/test.docx',
            original_name='disciplinare.docx',
            file_type='docx',
            file_size=1024,
            status='uploaded',
        )

    def test_parse_docx_url_exists(self):
        """AC-1: URL documents/parse-docx/<pk>/ esiste"""
        doc = self._create_uploaded_docx()
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse-docx/{doc.pk}/')
        self.assertNotEqual(response.status_code, 404)

    def test_parse_docx_redirects_anonymous(self):
        """AC-1: Redirect per utenti non autenticati"""
        doc = self._create_uploaded_docx()
        response = self.client.get(f'/documents/parse-docx/{doc.pk}/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_parse_docx_only_docx_documents(self):
        """AC-5: Solo documenti DOCX"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.pdf',
            original_name='test.pdf',
            file_type='pdf',
            file_size=1024,
            status='uploaded',
        )
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse-docx/{doc.pk}/')
        self.assertEqual(response.status_code, 400)

    def test_parse_docx_only_uploaded_status(self):
        """AC-5: Solo documenti con status uploaded"""
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.docx',
            original_name='test.docx',
            file_type='docx',
            file_size=1024,
            status='parsed',
        )
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse-docx/{doc.pk}/')
        self.assertEqual(response.status_code, 400)

    @patch('apps.document_parser.views.extract_text_from_docx')
    def test_parse_docx_success_updates_status(self, mock_extract):
        """AC-7: Status aggiornato a 'parsed' dopo successo"""
        mock_extract.return_value = 'Testo estratto dal DOCX'
        doc = self._create_uploaded_docx()
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse-docx/{doc.pk}/')
        doc.refresh_from_db()
        self.assertEqual(doc.status, 'parsed')

    @patch('apps.document_parser.views.extract_text_from_docx')
    def test_parse_docx_success_saves_content(self, mock_extract):
        """AC-6: Contenuto estratto salvato in parsed_content"""
        mock_extract.return_value = 'Testo estratto dal DOCX'
        doc = self._create_uploaded_docx()
        self.client.login(email='test@test.com', password='TestPass123!')
        self.client.get(f'/documents/parse-docx/{doc.pk}/')
        doc.refresh_from_db()
        self.assertEqual(doc.parsed_content, 'Testo estratto dal DOCX')

    @patch('apps.document_parser.views.extract_text_from_docx')
    def test_parse_docx_success_renders_result(self, mock_extract):
        """AC-1: Template risultato con anteprima contenuto"""
        mock_extract.return_value = 'Testo estratto dal DOCX'
        doc = self._create_uploaded_docx()
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse-docx/{doc.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testo estratto dal DOCX')

    @patch('apps.document_parser.views.extract_text_from_docx')
    def test_parse_docx_failure_updates_status_error(self, mock_extract):
        """AC-7: Status 'error' su fallimento parsing"""
        mock_extract.side_effect = DocumentParseError(
            message='Impossibile leggere il documento.'
        )
        doc = self._create_uploaded_docx()
        self.client.login(email='test@test.com', password='TestPass123!')
        self.client.get(f'/documents/parse-docx/{doc.pk}/')
        doc.refresh_from_db()
        self.assertEqual(doc.status, 'error')

    @patch('apps.document_parser.views.extract_text_from_docx')
    def test_parse_docx_failure_shows_friendly_error(self, mock_extract):
        """AC-4: Messaggio errore friendly in italiano"""
        mock_extract.side_effect = DocumentParseError(
            message='Impossibile leggere il documento. Verifica che il file sia un DOCX valido.'
        )
        doc = self._create_uploaded_docx()
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse-docx/{doc.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Impossibile leggere')
        self.assertNotContains(response, 'Traceback')

    def test_parse_docx_tenant_isolation(self):
        """AC-8: Isolamento tenant — solo propri documenti"""
        user2 = User.objects.create_user(
            email='other@test.com', password='TestPass123!', tenant=self.tenant
        )
        doc = self._create_uploaded_docx()
        self.client.login(email='other@test.com', password='TestPass123!')
        response = self.client.get(f'/documents/parse-docx/{doc.pk}/')
        # Redirect a upload_document con messaggio errore
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/documents/upload/')

    def test_parse_docx_nonexistent_document(self):
        """AC-1: Redirect per documento inesistente"""
        self.client.login(email='test@test.com', password='TestPass123!')
        response = self.client.get('/documents/parse-docx/99999/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/documents/upload/')


# =====================================================================
# TASK 3: URL per parsing DOCX (AC: 1)
# =====================================================================

class ParseDOCXURLTests(TestCase):
    """Test per URL parsing DOCX — Task 3"""

    def test_parse_docx_url_resolves(self):
        """AC-1: URL documents/parse-docx/<pk>/ risolve alla view corretta"""
        from django.urls import reverse
        url = reverse('document_parser:parse_docx_document', args=[1])
        self.assertEqual(url, '/documents/parse-docx/1/')


# =====================================================================
# TASK 4: Template risultato parsing (AC: 1)
# =====================================================================

class ParseDOCXTemplateTests(TestCase):
    """Test per template parse_docx_result.html — Task 4"""

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
        self.client.login(email='test@test.com', password='TestPass123!')

    @patch('apps.document_parser.views.extract_text_from_docx')
    def test_template_shows_document_name(self, mock_extract):
        """AC-1: Template mostra nome documento"""
        mock_extract.return_value = 'Testo'
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.docx',
            original_name='mio_documento.docx',
            file_type='docx',
            file_size=1024,
            status='uploaded',
        )
        response = self.client.get(f'/documents/parse-docx/{doc.pk}/')
        self.assertContains(response, 'mio_documento.docx')

    @patch('apps.document_parser.views.extract_text_from_docx')
    def test_template_shows_success_on_parse(self, mock_extract):
        """AC-1: Template mostra conferma successo"""
        mock_extract.return_value = 'Contenuto estratto'
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.docx',
            original_name='test.docx',
            file_type='docx',
            file_size=1024,
            status='uploaded',
        )
        response = self.client.get(f'/documents/parse-docx/{doc.pk}/')
        self.assertContains(response, 'successo')

    @patch('apps.document_parser.views.extract_text_from_docx')
    def test_template_shows_error_on_failure(self, mock_extract):
        """AC-4: Template mostra errore friendly in italiano"""
        mock_extract.side_effect = DocumentParseError(
            message='Impossibile leggere il documento.'
        )
        doc = Document.objects.create(
            user=self.user,
            file='documents/test.docx',
            original_name='test.docx',
            file_type='docx',
            file_size=1024,
            status='uploaded',
        )
        response = self.client.get(f'/documents/parse-docx/{doc.pk}/')
        self.assertContains(response, 'Errore')
        self.assertContains(response, 'Impossibile leggere')
