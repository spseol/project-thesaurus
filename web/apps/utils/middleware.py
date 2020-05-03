from django.http import HttpRequest
from django.middleware.locale import LocaleMiddleware as DjangoLocaleMiddleware

from apps import api


class LocaleMiddleware(DjangoLocaleMiddleware):
    """
    Custom locale middleware to avoid redirect 404s back to prefixed language version.
    """

    def process_response(self, request: HttpRequest, response):
        if request.resolver_match and request.resolver_match._func_path.startswith(api.__name__):
            return response

        return super().process_response(request, response)
