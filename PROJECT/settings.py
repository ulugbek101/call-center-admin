from os import makedirs
from pathlib import Path

from django.urls import reverse_lazy

from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()

makedirs(BASE_DIR / 'media', exist_ok=True)
makedirs(BASE_DIR / 'static', exist_ok=True)
makedirs(BASE_DIR / 'staticfiles', exist_ok=True)
makedirs(BASE_DIR / 'templates', exist_ok=True)

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

INSTALLED_APPS = [
    'unfold',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'phonenumber_field',
    'app_main',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PROJECT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'PROJECT.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST', default='db'),
        'PORT': env.str('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'app_main.User'

UNFOLD = {
    "SITE_TITLE": "Колл-центр | Админка",
    "SITE_HEADER": "KPI мониторинг",
    "SITE_SUBHEADER": "",
    "SITE_URL": None,
    "SHOW_HISTORY": True,
    "SHOW_BACK_BUTTON": True,
    "BORDER_RADIUS": "6px",
    "SIDEBAR": {
        "show_search": False,
        "command_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Офис",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Пользователи",
                        "icon": "people",
                        "badge_style": "solid",
                        "link": reverse_lazy("admin:app_main_user_changelist"),
                    }
                ],
            },
            {
                "title": "Менеджмент",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Этапы",
                        "icon": "timeline",
                        "link": reverse_lazy("admin:app_main_milestone_changelist"),
                    },
                    {
                        "title": "Мотивирующие фразы",
                        "icon": "keyboard_double_arrow_up",
                        "link": reverse_lazy("admin:app_main_motivationalphrase_changelist"),
                    }
                ],
            },
            {
                "title": "Вознаграждения и Наказания",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Выдать/Отнять балл",
                        "icon": "poker_chip",
                        "link": reverse_lazy("admin:app_main_point_changelist"),
                    }
                ],
            }
        ],
    },
}
