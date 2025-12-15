import os
from pathlib import Path

# -----------------------------------
# BASE DIRECTORY
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------
# SECURITY SETTINGS
# -----------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "%lhf_b36xo$zwh4&gs-kgu)5^8bjy3k$01g9$i2r2p+zvp-75_")

DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")

# -----------------------------------
# INSTALLED APPS
# -----------------------------------
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "drf_yasg",          # ✅ REQUIRED for Swagger & ReDoc
    "storages",

    # Project apps
    "categories",
    "authors",
    "news",
]


# -----------------------------------
# MIDDLEWARE
# -----------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------------
# URLS
# -----------------------------------
ROOT_URLCONF = "news_backend.urls"  # change if backend name is different

# -----------------------------------
# TEMPLATE SETTINGS
# -----------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # Custom template directory for overriding templates if needed
        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]



#------------------------------------
# WSGI
# -----------------------------------
WSGI_APPLICATION = "news_backend.wsgi.application"  # change if backend name is different

# -----------------------------------
# DATABASE (SQLite for now)
# -----------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -----------------------------------
# PASSWORD VALIDATORS
# -----------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------------
# INTERNATIONALIZATION
# -----------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -----------------------------------
# STATIC FILES
# -----------------------------------
# Static files (CSS, JS, images)
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/srideep_backend/static/'

# Django Rest Framework / Swagger static files
STATICFILES_DIRS = []


# -----------------------------------
# MEDIA STORAGE USING S3 + CLOUDFRONT
# -----------------------------------
MEDIA_URL = "https://d1nrpegwr01rgo.cloudfront.net/media/"
MEDIA_ROOT = None  # IMPORTANT: prevent local storage

# -----------------------------------
# AWS S3 STORAGE SETTINGS
# -----------------------------------
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "ap-south-1")
AWS_S3_SIGNATURE_VERSION = "s3v4"

AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False

# Django 5+ storage configuration
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# -----------------------------------
# DEFAULT PRIMARY KEY
# -----------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------
# LOGGING (OPTIONAL BUT USEFUL)
# -----------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}


#-----------------
#REST FRAME WORK
#----------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",

    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],

    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}
