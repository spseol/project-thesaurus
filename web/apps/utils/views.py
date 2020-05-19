from typing import Type

from django.conf import settings
from django.db.models import Choices
from django.http import HttpRequest
from django.views.defaults import server_error as django_server_error
from rest_framework.exceptions import server_error as drf_server_error
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin


class ModelChoicesOptionsView(ViewSetMixin, APIView):
    choices: Type[Choices] = None
    permission_classes = (IsAuthenticated,)  # no queryset, not specific perms

    def list(self, request, *args, **kwargs):
        return Response(map(
            lambda choice: dict(value=choice[0], text=choice[1]),
            self.choices.choices,
        ))


def server_error(request: HttpRequest, *args, **kwargs):
    if settings.API_URL_PATTERN.match(request.path_info):
        return drf_server_error(request, *args, **kwargs)

    return django_server_error(request, *args, **kwargs)
