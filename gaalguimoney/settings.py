"""
Django settings for gaalguimoney project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
import dj_database_url
from firebase_admin import initialize_app

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-file.json"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_-6!zz)b&gfsbz_p691cp=rvdoaivsk_v105&gzuvro!x4(=hh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'staff',
    'pay',
    'phonenumber_field',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'qr_code',
   'django_celery_results',
   'django_celery_beat',
   "fcm_django",

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gaalguimoney.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
AUTH_USER_MODEL = 'user.User'

WSGI_APPLICATION = 'gaalguimoney.wsgi.application'
ASGI_APPLICATION = "gaalguimoney.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gaalguimoney',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER':'xspibzvoksuwoa',
        'NAME': 'd6vnhif27vpeck',
        'PASSWORD':'68bfb8e8150f8a88b990c69a13df5d1b597ae6d234979caf3fb098456e5400f3',
        'HOST':'ec2-3-231-82-226.compute-1.amazonaws.com',
        'PORT':'5432'
    } 
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'] = dj_database_url.config(default='postgres://xspibzvoksuwoa:68bfb8e8150f8a88b990c69a13df5d1b597ae6d234979caf3fb098456e5400f3@ec2-3-231-82-226.compute-1.amazonaws.com:5432/d6vnhif27vpeck')
DATABASES['default'].update(db_from_env)
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
#CORS_ORIGIN_ALLOW_ALL = True

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, 'static'),
)
MEDIA_URL ='/media/'
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOWED_ORIGINS = [

    "http://localhost:3000",
    "http://localhost:8100",
    "https://gaalguimoneyfronti.herokuapp.com",
    "https://10.0.2.2:8080"
 ]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer','JWT'),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

#CELERY SETTINGS

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_RESULT_SERIALIZER='json'
CELERY_TASK_SERIALIZER= 'json'
CELERY_TIMEZONE='Asia/Yekaterinburg'
cELERY_RESULT_BACKEND='django-db'

FCM_DJANGO_SETTINGS = {
     # default: _('FCM Django')
    "APP_VERBOSE_NAME": "gaalguishop",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
    "FCM_SERVER_KEY": "BE_TlKzjr6C52EEVsyJWYWCPPZVho_UdSDsKy2Gx2as8dQevvItT8xUCJIkaPnaiiLGD6_D_E5EoXrrcv3votao",
    "UPDATE_ON_DUPLICATE_REG_ID": True
}

'''CELERY_BEAT_SCHEDULE = {
    "scheduled_task": {
        "task": "task1.tasks.add",
        "schedule": 5.0,
        "args": (10, 10),
    },
    "database": {
        "task": "task3.tasks.bkup",
        "schedule": 5.0,
    },
}'''
'''
#web: daphne gaalguimoney.asgi:application --port $PORT --bind 0.0.0.0 -v2
#celeryworker2: celery -A gaalguimoney.celery worker & celery -A gaalguimoney beat -l INFO & wait -n
'''