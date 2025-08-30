import os
from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# Variáveis sensíveis e ambiente
# -------------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'sua-chave-secreta-teste')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# -------------------------------
# Aplicações instaladas
# -------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Necessário para arquivos estáticos
    'core',
    'livros',
]

# -------------------------------
# Middlewares
# -------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------------
# Validação de senhas (desabilitada para teste)
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

# Diretórios de arquivos estáticos locais
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Diretório onde os arquivos estáticos serão coletados no servidor
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

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
