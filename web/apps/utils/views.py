from typing import Type

from django.db.models import Choices
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
