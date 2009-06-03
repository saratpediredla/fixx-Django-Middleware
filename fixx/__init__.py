from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings

if settings.FIXX_URL is None or \
   settings.FIXX_USER is None or \
   settings.FIXX_PASSWORD is None or \
   settings.FIXX_DEFAULT_AREA is None:
    raise MiddlewareNotUsed