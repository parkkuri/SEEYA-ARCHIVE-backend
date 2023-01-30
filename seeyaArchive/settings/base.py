import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "seat_reviews",
    "concert_halls",
    "accounts",
    # 'sorl.thumbnail',
    "drf_yasg",
    "corsheaders",
    "rest_framework",
    "django.contrib.sites",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# .env 파일 환경변수로 불러오로
load_dotenv(".env")


# Application definition
SECRET_KEY = os.getenv("SECRET_KEY")

# 카카오 로그인
SOCIAL_OAUTH_CONFIG = {
    "MY_AWS_SECRET_ACCESS_KEY": os.getenv("MY_AWS_SECRET_ACCESS_KEY"),
    "MY_AWS_ACCESS_KEY_ID": os.getenv("MY_AWS_ACCESS_KEY_ID"),
    "KAKAO_REST_API_KEY": os.getenv("KAKAO_REST_API_KEY"),
    "KAKAO_REDIRECT_URI": os.getenv("KAKAO_REDIRECT_URI"),
    "KAKAO_SECRET_KEY": os.getenv("KAKAO_SECRET_KEY"),
    "KAKAO_ADMIN_KEY": os.getenv("KAKAO_ADMIN_KEY"),
    "AWS_REGION": os.getenv("AWS_REGION"),
    "AWS_ROOT_STORAGE_BUCKET_NAME": os.getenv("AWS_ROOT_STORAGE_BUCKET_NAME"),
}

SITE_ID = 1
LOGIN_REDIRECT_URL = "/"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


ROOT_URLCONF = "seeyaArchive.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "seeyaArchive.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"
