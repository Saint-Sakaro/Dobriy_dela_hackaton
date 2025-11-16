from .base import *  # noqa

DEBUG = True

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

