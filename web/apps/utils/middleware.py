import re
from operator import methodcaller

from django.conf import settings
from django.http import HttpRequest
from django.middleware.locale import LocaleMiddleware as DjangoLocaleMiddleware


class LocaleMiddleware(DjangoLocaleMiddleware):
    """
    Custom locale middleware to avoid redirect 404s back to prefixed language version.
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)

        self._ignore_urls = tuple(map(re.compile, settings.LOCALE_MIDDLEWARE_IGNORE_URLS))

    def process_response(self, request: HttpRequest, response):
        if any(map(methodcaller('match', request.path), self._ignore_urls)):
            return response

        return super().process_response(request, response)
