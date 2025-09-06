import os
from pathlib import Path
import dj_database_url

# Caminho base
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# Variáveis sensíveis e ambiente
# -------------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'sua-chave-secreta-teste')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Hosts permitidos
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'entrelinhas-dtm8.onrender.com',
    '.onrender.com',
]

# -------------------------------
# Aplicações instaladas
# -------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'livros',
]

# -------------------------------
# Middlewares
# -------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # importante no Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------------
# URLs e templates
# -------------------------------
ROOT_URLCONF = 'entrelinhas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'entrelinhas.wsgi.application'

# -------------------------------
# Banco de dados
# -------------------------------
if os.environ.get("DATABASE_URL"):  # Render ou produção
    DATABASES = {
        "default": dj_database_url.parse(
            os.environ["DATABASE_URL"],
            conn_max_age=600,
            ssl_require=True
        )
    }
else:  # Local (SQLite)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -------------------------------
# Validação de senhas
# -------------------------------
AUTH_PASSWORD_VALIDATORS = []

# -------------------------------
# Internacionalização
# -------------------------------
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# -------------------------------
# Arquivos estáticos
# -------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Whitenoise para produção
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -------------------------------
# Redirecionamentos de login
# -------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'minha_estante'
LOGOUT_REDIRECT_URL = 'login'

# -------------------------------
# Campo automático padrão
# -------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'