"""
Test suite per Story 1.1 — Setup Django Project.

Satisfies: AC-01, AC-02, AC-03, AC-04
Covers:
    AC-01 — Struttura modulare Django (core/llm, apps/*)
    AC-02 — Configurazione tramite variabili d'ambiente
    AC-03 — Logging multi-livello
    AC-04 — Custom exceptions con messaggi in italiano
"""

import logging
import os
from pathlib import Path

import django
from django.test import SimpleTestCase, TestCase, override_settings

# ---------------------------------------------------------------------------
# Costanti
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # /a0/usr/projects/ai_tender


# ===========================================================================
# AC-01: Struttura modulare del progetto
# ===========================================================================
class TestModularStructure(SimpleTestCase):
    """Verifica che la struttura modulare del progetto esista su disco.

    Satisfies: AC-01
    """

    def test_core_package_exists(self):
        """AC-01: core/__init__.py deve esistere."""
        self.assertTrue(
            (BASE_DIR / 'core' / '__init__.py').exists(),
            "core/__init__.py non trovato",
        )

    def test_core_llm_package_exists(self):
        """AC-01: core/llm/__init__.py deve esistere."""
        self.assertTrue(
            (BASE_DIR / 'core' / 'llm' / '__init__.py').exists(),
            "core/llm/__init__.py non trovato",
        )

    def test_apps_package_exists(self):
        """AC-01: apps/__init__.py deve esistere."""
        self.assertTrue(
            (BASE_DIR / 'apps' / '__init__.py').exists(),
            "apps/__init__.py non trovato",
        )

    def _assert_app_structure(self, app_name: str):
        """Helper: verifica che un'app abbia __init__.py, models.py, views.py."""
        app_dir = BASE_DIR / 'apps' / app_name
        for fname in ('__init__.py', 'models.py', 'views.py', 'apps.py'):
            with self.subTest(app=app_name, file=fname):
                self.assertTrue(
                    (app_dir / fname).exists(),
                    f"apps/{app_name}/{fname} non trovato",
                )

    def test_pipeline_app_structure(self):
        """AC-01: apps/pipeline/ struttura completa."""
        self._assert_app_structure('pipeline')

    def test_document_parser_app_structure(self):
        """AC-01: apps/document_parser/ struttura completa."""
        self._assert_app_structure('document_parser')

    def test_field_analyzer_app_structure(self):
        """AC-01: apps/field_analyzer/ struttura completa."""
        self._assert_app_structure('field_analyzer')

    def test_questionnaire_app_structure(self):
        """AC-01: apps/questionnaire/ struttura completa."""
        self._assert_app_structure('questionnaire')

    def test_compiler_app_structure(self):
        """AC-01: apps/compiler/ struttura completa."""
        self._assert_app_structure('compiler')

    def test_installed_apps_contains_modular_apps(self):
        """AC-01: INSTALLED_APPS deve contenere tutte le app modulari."""
        from django.conf import settings
        expected_apps = [
            'apps.pipeline',
            'apps.document_parser',
            'apps.field_analyzer',
            'apps.questionnaire',
            'apps.compiler',
        ]
        for app in expected_apps:  # AC-01: verifica ogni app
            with self.subTest(app=app):
                self.assertIn(
                    app,
                    settings.INSTALLED_APPS,
                    f"{app} non trovato in INSTALLED_APPS",
                )


# ===========================================================================
# AC-02: Configurazione tramite variabili d'ambiente
# ===========================================================================
class TestEnvironmentConfiguration(SimpleTestCase):
    """Verifica che settings.py legga correttamente da env files.

    Satisfies: AC-02
    """

    def test_env_dir_points_to_a0proj(self):
        """AC-02: ENV_DIR deve puntare a .a0proj/."""
        from django.conf import settings
        expected = BASE_DIR / '.a0proj'
        self.assertEqual(
            settings.ENV_DIR,
            expected,
            f"ENV_DIR = {settings.ENV_DIR}, atteso {expected}",
        )

    def test_secret_key_is_set(self):
        """AC-02: SECRET_KEY deve essere non vuoto."""
        from django.conf import settings
        self.assertTrue(
            bool(settings.SECRET_KEY),
            "SECRET_KEY non impostato",
        )

    def test_allowed_hosts_is_list(self):
        """AC-02: ALLOWED_HOSTS deve essere una lista non vuota."""
        from django.conf import settings
        self.assertIsInstance(settings.ALLOWED_HOSTS, list)
        self.assertGreater(len(settings.ALLOWED_HOSTS), 0)

    def test_database_engine_is_sqlite(self):
        """AC-02: DATABASE default engine deve essere sqlite3 (MVP)."""
        from django.conf import settings
        self.assertIn(
            'sqlite3',
            settings.DATABASES['default']['ENGINE'],
        )

    def test_variables_env_file_exists(self):
        """AC-02: Il file variables.env deve esistere in .a0proj/."""
        env_file = BASE_DIR / '.a0proj' / 'variables.env'
        self.assertTrue(env_file.exists(), f"{env_file} non trovato")

    def test_secrets_env_file_exists(self):
        """AC-02: Il file secrets.env deve esistere in .a0proj/."""
        env_file = BASE_DIR / '.a0proj' / 'secrets.env'
        self.assertTrue(env_file.exists(), f"{env_file} non trovato")


# ===========================================================================
# AC-03: Logging multi-livello
# ===========================================================================
class TestLoggingConfiguration(SimpleTestCase):
    """Verifica che il logging sia configurato con tutti i livelli richiesti.

    Satisfies: AC-03
    """

    def test_logging_config_present(self):
        """AC-03: LOGGING deve essere definito in settings."""
        from django.conf import settings
        self.assertTrue(
            hasattr(settings, 'LOGGING'),
            "LOGGING non trovato in settings",
        )
        self.assertIsInstance(settings.LOGGING, dict)

    def test_logging_has_console_handler(self):
        """AC-03: deve esistere un handler 'console'."""
        from django.conf import settings
        self.assertIn('console', settings.LOGGING.get('handlers', {}))

    def test_logging_has_file_info_handler(self):
        """AC-03: deve esistere un handler 'file_info' per i log INFO."""
        from django.conf import settings
        self.assertIn('file_info', settings.LOGGING.get('handlers', {}))

    def test_logging_has_file_error_handler(self):
        """AC-03: deve esistere un handler 'file_error' per WARNING+."""
        from django.conf import settings
        self.assertIn('file_error', settings.LOGGING.get('handlers', {}))

    def test_ai_tender_logger_exists(self):
        """AC-03: logger 'ai_tender' deve essere configurato."""
        from django.conf import settings
        self.assertIn('ai_tender', settings.LOGGING.get('loggers', {}))

    def test_all_module_loggers_configured(self):
        """AC-03: tutti i logger delle app modulari devono essere configurati."""
        from django.conf import settings
        expected_loggers = [
            'apps.pipeline',
            'apps.document_parser',
            'apps.field_analyzer',
            'apps.questionnaire',
            'apps.compiler',
            'core',
        ]
        for logger_name in expected_loggers:  # AC-03: ogni logger deve esistere
            with self.subTest(logger=logger_name):
                self.assertIn(
                    logger_name,
                    settings.LOGGING.get('loggers', {}),
                    f"Logger '{logger_name}' non configurato",
                )

    def test_log_directory_created(self):
        """AC-03: La directory logs/ deve essere creata automaticamente."""
        log_dir = BASE_DIR / 'logs'
        self.assertTrue(log_dir.is_dir(), "Directory logs/ non creata")

    def test_all_log_levels_functional(self):
        """AC-03: Tutti i livelli (DEBUG/INFO/WARNING/ERROR/CRITICAL) devono essere utilizzabili."""
        logger = logging.getLogger('ai_tender')
        # Verifica che il logger accetti tutti i livelli senza eccezioni
        try:
            logger.debug("[TEST] Livello DEBUG funzionante")
            logger.info("[TEST] Livello INFO funzionante")
            logger.warning("[TEST] Livello WARNING funzionante")
            logger.error("[TEST] Livello ERROR funzionante")
            logger.critical("[TEST] Livello CRITICAL funzionante")
        except Exception as exc:
            self.fail(f"Logger ha sollevato un'eccezione inattesa: {exc}")


# ===========================================================================
# AC-04: Custom exceptions
# ===========================================================================
class TestCustomExceptions(SimpleTestCase):
    """Verifica le eccezioni personalizzate definite in core/exceptions.py.

    Satisfies: AC-04
    """

    def setUp(self):
        from core.exceptions import (
            AiTenderBaseError,
            CompilationError,
            DocumentParseError,
            FieldAnalysisError,
        )
        self.AiTenderBaseError = AiTenderBaseError
        self.DocumentParseError = DocumentParseError
        self.FieldAnalysisError = FieldAnalysisError
        self.CompilationError = CompilationError

    def test_document_parse_error_is_exception(self):
        """AC-04: DocumentParseError deve essere un'eccezione."""
        self.assertTrue(issubclass(self.DocumentParseError, Exception))

    def test_field_analysis_error_is_exception(self):
        """AC-04: FieldAnalysisError deve essere un'eccezione."""
        self.assertTrue(issubclass(self.FieldAnalysisError, Exception))

    def test_compilation_error_is_exception(self):
        """AC-04: CompilationError deve essere un'eccezione."""
        self.assertTrue(issubclass(self.CompilationError, Exception))

    def test_all_inherit_from_base(self):
        """AC-04: Tutte le eccezioni devono ereditare da AiTenderBaseError."""
        for exc_class in (
            self.DocumentParseError,
            self.FieldAnalysisError,
            self.CompilationError,
        ):
            with self.subTest(exc=exc_class.__name__):
                self.assertTrue(
                    issubclass(exc_class, self.AiTenderBaseError),
                    f"{exc_class.__name__} non eredita da AiTenderBaseError",
                )

    def test_document_parse_error_has_italian_default_message(self):
        """AC-04: DocumentParseError default message deve essere in italiano."""
        exc = self.DocumentParseError()
        # Verifica che il messaggio non sia vuoto e sia in italiano (contiene parole chiave)
        self.assertTrue(len(str(exc)) > 0)
        self.assertIn('documento', str(exc).lower())

    def test_field_analysis_error_has_italian_default_message(self):
        """AC-04: FieldAnalysisError default message deve essere in italiano."""
        exc = self.FieldAnalysisError()
        self.assertTrue(len(str(exc)) > 0)
        self.assertIn('analisi', str(exc).lower())

    def test_compilation_error_has_italian_default_message(self):
        """AC-04: CompilationError default message deve essere in italiano."""
        exc = self.CompilationError()
        self.assertTrue(len(str(exc)) > 0)
        self.assertIn('compilazione', str(exc).lower())

    def test_custom_message_overrides_default(self):
        """AC-04: Messaggio personalizzato deve sovrascrivere il default."""
        msg = "Documento PDF corrotto"
        exc = self.DocumentParseError(message=msg)
        self.assertEqual(str(exc), msg)

    def test_detail_not_exposed_in_str(self):
        """AC-04: Il dettaglio tecnico NON deve apparire in __str__."""
        detail = "Internal SQL traceback xyz"
        exc = self.DocumentParseError(message="Errore", detail=detail)
        self.assertNotIn(detail, str(exc))  # AC-04: stack trace non esposto

    def test_exceptions_are_raiseable(self):
        """AC-04: Tutte le eccezioni devono essere sollevabili correttamente."""
        for exc_class in (
            self.DocumentParseError,
            self.FieldAnalysisError,
            self.CompilationError,
        ):
            with self.subTest(exc=exc_class.__name__):
                with self.assertRaises(exc_class):
                    raise exc_class(message="Errore di test")

    def test_exceptions_catchable_as_base(self):
        """AC-04: Eccezioni specifiche devono essere catturabili come AiTenderBaseError."""
        for exc_class in (
            self.DocumentParseError,
            self.FieldAnalysisError,
            self.CompilationError,
        ):
            with self.subTest(exc=exc_class.__name__):
                with self.assertRaises(self.AiTenderBaseError):
                    raise exc_class(message="Errore di test")
