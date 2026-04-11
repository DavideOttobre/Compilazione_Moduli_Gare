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
BASE_DIR = Path(__file__).resolve().parent.parent

ENV_DIR = BASE_DIR / '.a0proj'

# ---------------------------------------------------------------------------
# AC-02: Configurazione tramite variabili d'ambiente (variables.env + secrets.env)
# ---------------------------------------------------------------------------
_variables_env_path = ENV_DIR / 'variables.env'
_secrets_env_path = ENV_DIR / 'secrets.env'

if _variables_env_path.exists():
    _config = Config(RepositoryEnv(str(_variables_env_path)))
else:
    from decouple import config as _config  # type: ignore  # noqa: F811

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
SECRET_KEY = _get(
    'DJANGO_SECRET_KEY',
    default='django-insecure-change-me-in-production'
)

DEBUG = _get('DJANGO_DEBUG', default='True') in ('True', 'true', '1', True)

_allowed_hosts_raw = _get('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_raw.split(',') if h.strip()]

import base64
import os
_default_encryption_key = base64.urlsafe_b64encode(os.urandom(32)).decode()
FIELD_ENCRYPTION_KEY = _get('FIELD_ENCRYPTION_KEY', default=_default_encryption_key)


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
    'apps.accounts',
]
AUTH_USER_MODEL = 'accounts.UserCustom'

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
# MEDIA FILES (Story 2.1: Upload documenti)
# ---------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ---------------------------------------------------------------------------
# DEFAULT AUTO FIELD
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------------------------------------------------------------------
# AC-03: Configurazione LOGGING multi-livello
# ---------------------------------------------------------------------------
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {module}:{lineno} -- {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[{levelname}] {name}: {message}',
            'style': '{',
        },
    },

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'ai_tender.log'),
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'file_error': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'errors.log'),
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'ai_tender': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
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

    'root': {
        'handlers': ['console', 'file_error'],
        'level': 'WARNING',
    },
}


# ---------------------------------------------------------------------------
# SESSION CONFIGURATION (Story 1.3 - Task 3)
# NFR7: Session timeout 30 minuti
# ---------------------------------------------------------------------------
SESSION_COOKIE_AGE = 1800
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
