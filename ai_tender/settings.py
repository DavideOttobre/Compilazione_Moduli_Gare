"""
Django settings per il progetto ai_tender.

Satisfies: AC-01 (struttura modulare), AC-02 (env vars), AC-03 (logging)

Generato con Django 6.0.3.
Documentazione: https://docs.djangoproject.com/en/6.0/topics/settings/
"""

from pathlib import Path
from decouple import Config, RepositoryEnv

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cartella che contiene i file .env del progetto
ENV_DIR = BASE_DIR / '.a0proj'

# ---------------------------------------------------------------------------
# AC-02: Configurazione tramite variabili d'ambiente (variables.env + secrets.env)
# ---------------------------------------------------------------------------
# Carica variables.env per le variabili operative
_variables_env_path = ENV_DIR / 'variables.env'
_secrets_env_path = ENV_DIR / 'secrets.env'

# Usa variables.env come sorgente principale; fallback ai valori di default
if _variables_env_path.exists():
    _config = Config(RepositoryEnv(str(_variables_env_path)))
else:
    from decouple import config as _config  # type: ignore  # noqa: F811

# Secrets sovrascrivono le variabili se presenti
if _secrets_env_path.exists():
    _secrets_config = Config(RepositoryEnv(str(_secrets_env_path)))
else:
    _secrets_config = None


def _get(key, default=None, cast=None):
    """Legge prima da secrets.env, poi da variables.env, poi usa il default."""
    if _secrets_config is not None:
        try:
            val = _secrets_config(key, default=None, cast=cast)
            if val is not None:
                return val
        except Exception:
            pass
    try:
        if cast:
            return _config(key, default=default, cast=cast)
        return _config(key, default=default)
    except Exception:
        return default


# ---------------------------------------------------------------------------
# SICUREZZA
# ---------------------------------------------------------------------------
# AC-02: SECRET_KEY letta da secrets.env
SECRET_KEY = _get(
    'DJANGO_SECRET_KEY',
    default='django-insecure-change-me-in-production'
)

# AC-02: DEBUG letto da variables.env
DEBUG = _get('DJANGO_DEBUG', default='True') in ('True', 'true', '1', True)

# AC-02: ALLOWED_HOSTS letto da variables.env
_allowed_hosts_raw = _get('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_raw.split(',') if h.strip()]


# ---------------------------------------------------------------------------
# AC-01: Applicazioni installate — struttura modulare
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # AC-01: app modulari del progetto ai_tender
    'apps.pipeline',
    'apps.document_parser',
    'apps.field_analyzer',
    'apps.questionnaire',
    'apps.compiler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ai_tender.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ai_tender.wsgi.application'


# ---------------------------------------------------------------------------
# DATABASE — AC-01: SQLite per MVP
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / _get('DB_NAME', default='db.sqlite3'),
    }
}


# ---------------------------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------------------------------------------------
# INTERNAZIONALIZZAZIONE
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


# ---------------------------------------------------------------------------
# DEFAULT AUTO FIELD
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------------------------------------------------------------------
# AC-03: Configurazione LOGGING multi-livello
# DEBUG / INFO / WARNING / ERROR / CRITICAL
# Handler: console + file
# ---------------------------------------------------------------------------
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # Formatter dettagliato per file, compatto per console
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {module}:{lineno} — {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[{levelname}] {name}: {message}',
            'style': '{',
        },
    },

    # Filtri
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    # Handler: console (DEBUG+) e file separati per INFO e ERROR
    'handlers': {
        # AC-03: console — tutti i livelli in sviluppo
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # AC-03: file generale — INFO e superiori
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'ai_tender.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        # AC-03: file errori — WARNING e superiori
        'file_error': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'errors.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },

    # Logger radice e specifici per ogni app
    'loggers': {
        # AC-03: logger Django — WARNING su console, INFO su file
        'django': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        # AC-03: logger specifico ai_tender — DEBUG completo
        'ai_tender': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # AC-03: logger per ogni app modulare
        'apps.pipeline': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.document_parser': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.field_analyzer': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.questionnaire': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.compiler': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },

    # Root logger — catch-all
    'root': {
        'handlers': ['console', 'file_error'],
        'level': 'WARNING',
    },
}
