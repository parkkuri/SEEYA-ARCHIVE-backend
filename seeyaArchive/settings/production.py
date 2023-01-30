import os

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    os.getenv("SERVER_HOST"),
    os.getenv("DOMAIN_GENERAL"),
    os.getenv("DOMAIN_API"),
    os.getenv("DOMAIN"),
]

SESSION_COOKIE_DOMAIN = ".seeya-archive.com"
SESSION_COOKIE_NAME = "sessionid"
CSRF_COOKIE_DOMAIN = ".seeya-archive.com"
CSRF_COOKIE_NAME = "csrftoken"

CORS_ORIGIN_WHITELIST = (
    os.getenv("DOMAIN_SCHEME"),
    os.getenv("DOMAIN_API_SCHEME"),
    os.getenv("DOMAIN_WWW_SCHEME"),
    "http://localhost:3000",
)

CSRF_TRUSTED_ORIGINS = (
    os.getenv("DOMAIN_SCHEME"),
    os.getenv("DOMAIN_API_SCHEME"),
    os.getenv("DOMAIN_WWW_SCHEME"),
    "http://localhost:3000",
)


CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)


# S3 설정을 위한 변수
AWS_ACCESS_KEY_ID = os.getenv("MY_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("MY_AWS_SECRET_ACCESS_KEY")
AWS_ROOT_STORAGE_BUCKET_NAME = os.getenv("AWS_ROOT_STORAGE_BUCKET_NAME")
AWS_STORAGE_BUCKET_NAME = 'review-images'
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_CUSTOM_DOMAIN = "https://%s.s3.%s.amazonaws.com/" % (AWS_ROOT_STORAGE_BUCKET_NAME, AWS_REGION)

STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

STATIC_URL = "/static/"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

SESSION_COOKIE_DOMAIN = os.getenv("DOMAIN")
SESSION_COOKIE_NAME = "sessionid"
CSRF_COOKIE_DOMAIN = os.getenv("DOMAIN")
CSRF_COOKIE_NAME = "csrftoken"