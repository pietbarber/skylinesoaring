"""
Django settings for skylinesoaring project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

from django.shortcuts import redirect

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static", 
]



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# That's why we put it in .env and .env is in .gitignore ! 

import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY not set in environment!")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap4",
    "social_django",
    "tinymce",
    "members",
    "instructors",
    "logsheet"
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/members/'
LOGOUT_REDIRECT_URL = 'login'
AUTH_USER_MODEL = 'members.Member'


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

from django.contrib.auth.decorators import login_required

LOGIN_REQUIRED_MIDDLEWARE = (
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

def login_required_middleware(get_response):
    def middleware(request):
        if not request.user.is_authenticated and not request.path.startswith('/accounts/login/'):
            return redirect('login')
        return get_response(request)
    return middleware

ROOT_URLCONF = "skylinesoaring.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [BASE_DIR / "templates"],  # <- this line is key
        'APP_DIRS': True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = "skylinesoaring.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_PIPELINE = (
    # Standard steps
    'social_core.pipeline.social_auth.social_details',         # Get user details from provider
    'social_core.pipeline.social_auth.social_uid',             # Get provider UID
    'social_core.pipeline.social_auth.auth_allowed',           # Check if auth is allowed
    'social_core.pipeline.social_auth.social_user',            # Try to find existing social user

    # 🔁 NEW: Associate by email if not linked yet (password-first → OAuth2)
    'social_core.pipeline.social_auth.associate_by_email',

    # 🛠️ Custom steps — insert after association
    'members.pipeline.debug_pipeline_data',                    # Log details
    'members.pipeline.create_username',                        # Create proper username format
    'social_core.pipeline.user.get_username',                  # Default username getter
    'social_core.pipeline.user.create_user',                   # Create user if not found
    'members.pipeline.set_default_membership_status',          # Set membership status
    'members.pipeline.fetch_google_profile_picture',           # Fetch profile picture from Google

    # Standard steps to finalize
    'social_core.pipeline.social_auth.associate_user',         # Link social to user
    'social_core.pipeline.social_auth.load_extra_data',        # Load extras
    'social_core.pipeline.user.user_details',                  # Update user fields
)





# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # Or your real domain in production

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


from django.conf import settings
from django.conf.urls.static import static

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'social': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

handler403 = 'members.views.custom_permission_denied_view'

TINYMCE_DEFAULT_CONFIG = {
    "height": 500,
    "menubar": "file edit view insert format tools table help",
    "plugins": "image link media code lists",
    "toolbar": (
        "undo redo | bold italic underline | alignleft aligncenter alignright | "
        "bullist numlist outdent indent | link image media | code"
    ),
    "image_caption": True,
    "automatic_uploads": True,
    "file_picker_types": "image",
    "images_upload_url": "/members/tinymce-upload/",
    "images_upload_credentials": True,  # include CSRF token
}

