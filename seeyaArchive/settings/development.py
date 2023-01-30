from .base import *

DEBUG = False
ALLOWED_HOSTS = []


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AWS_ROOT_STORAGE_BUCKET_NAME = os.getenv("AWS_ROOT_STORAGE_BUCKET_NAME")
AWS_STORAGE_BUCKET_NAME = 'dev-review-images'
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_CUSTOM_DOMAIN = "https://%s.s3.%s.amazonaws.com/" % (AWS_ROOT_STORAGE_BUCKET_NAME, AWS_REGION)