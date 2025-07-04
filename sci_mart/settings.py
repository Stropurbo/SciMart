from pathlib import Path
from datetime import timedelta
from decouple import config
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-zu2un4x34&7zlqf_1gqoqv(6^c70lnn61qrul1_8(7-5&la3yw'

DEBUG = False

ALLOWED_HOSTS = [".vercel.app", '127.0.0.1']
AUTH_USER_MODEL = 'users.User'


# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'drf_yasg',
    'api',
    'order',
    'product',
    'users',
    'rest_framework',
    "debug_toolbar",
    'django_filters',
    'djoser',
    
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware', 
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sci_mart.urls'

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

WSGI_APPLICATION = 'sci_mart.wsgi.app'

CORS_ALLOWED_ORIGINS = [
"http://localhost:5173",
"https://sci-mart.vercel.app",
"https://scimart-client.vercel.app",
]
    


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('dbname'),
        'USER': config('user'),
        'PASSWORD': config('password'),
        'HOST': config('host'),
        'PORT': config('port'),
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

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


# Configuration for cloudinary storage       
cloudinary.config( 
    cloud_name = config('cloudname'), 
    api_key = config('cloudapikey'),  
    api_secret = config('apisecret'),
    secure=True
)

#Media Storage setting
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


BACKEND_URL = config('BACKEND_URL')
FRONTEND_URL = config('FRONTEND_URL')


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
# STATIC_FILES_DIR = BASE_DIR / 'static'
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
     'COERCE_DECIMAL_TO_STRING' : False,
     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
     'PAGE_SIZE' : 10,
     'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ]
}
SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),

}

DJOSER = {
    'EMAIL_FRONTEND_PROTOCOL' : config('FRONTEND_PROTOCOL'),
    'EMAIL_FRONTEND_DOMAIN': config('FRONTEND_DOMAIN'),
    'EMAIL_FRONTEND_SITE_NAME': 'SciMart',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS': {
        'user_create': 'users.serializers.UserCreateSerializers',
        'current_user': 'users.serializers.CurrentUserSerializers',
    },
}

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Enter your jwt token in the format: `JWT <token>`'
      }
   }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
