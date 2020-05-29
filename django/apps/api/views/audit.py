from typing import Type

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.utils.translation import ugettext as _
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.audit.models import AuditLog
from apps.audit.serializers import AuditLogSerializer


class AuditLogViewSet(ViewSet):
    queryset = AuditLog.objects.all()  # to correct perms check

    @action(
        detail=False,
        url_path=r'for-instance/(?P<model_name>[^/.]+\.[^/.]+)/(?P<model_pk>[^/.]+)'
    )
    def for_instance(self, request, model_name, model_pk, *args, **kwargs):
        try:
            model: Type[Model] = apps.get_model(model_name)
        except LookupError:
            raise NotFound(_('Unknown model to audit.'))

        try:
            instance = model._base_manager.get_queryset().get(pk=model_pk)
        except model.DoesNotExist:
            instance = model(pk=model_pk)

        return Response(
            data=dict(
                results=AuditLogSerializer(
                    instance=AuditLog.objects.for_instance(instance=instance).select_related('user'),
                    many=True
                ).data,
                __model__=model._meta.verbose_name,
                __class__=model.__name__,
            )
        )

    @action(
        detail=False,
        url_path=r'by-user/(?P<user_pk>[^/.]+)'
    )
    def by_user(self, request, user_pk, *args, **kwargs):
        user = get_object_or_404(
            queryset=get_user_model().objects.all(),
            pk=user_pk
        )

        return Response(
            data=dict(
                results=AuditLogSerializer(
                    instance=AuditLog.objects.by_user(user=user).select_related('user'),
                    many=True,
                ).data,
            )
        )
