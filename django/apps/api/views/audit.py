from operator import itemgetter
from typing import Type, Iterable

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Model, ManyToOneRel, ManyToManyRel, ManyToManyField
from django.db.models.base import ModelBase
from django.utils.translation import ugettext as _
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.audit.models import AuditLog
from apps.audit.serializers import AuditLogSerializer


class AuditViewSet(GenericViewSet):
    queryset = AuditLog.objects.all()  # to correct perms check
    serializer_class = AuditLogSerializer

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
            __str__ = str(instance)
        except model.DoesNotExist:
            instance = model(pk=model_pk)
            try:
                __str__ = str(instance)
            except Exception:
                __str__ = ''

        queryset = AuditLog.objects.for_instance(instance=instance).select_related('user')
        queryset = self.paginate_queryset(queryset=queryset)
        response: Response = self.get_paginated_response(data=self.serializer_class(
            instance=queryset,
            many=True
        ).data)

        return Response(
            data=dict(
                **response.data,
                __model__=model._meta.verbose_name,
                __class__=model.__name__,
                __str__=__str__,
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

    @action(
        detail=False,
    )
    def mappings(self, request, *args, **kwargs):
        models: Iterable[ModelBase] = apps.get_models()

        return Response(
            data=dict(
                # supervisor_id -> account.user
                # thesis_id -> thesis.thesis
                foreign_key_to_model=dict(
                    (field, model._meta.label_lower)
                    for model in models
                    for field in AuditLog.objects.get_referencing_columns(model._meta)
                ),
                # thesis_thesis:
                # # title -> 'Thesis title'
                # # supervisor_id -> 'Supervisor'
                table_columns_to_labels=dict(
                    (
                        model._meta.db_table,
                        dict(
                            (field.column, field.verbose_name)
                            for field in model._meta.get_fields()
                            if not isinstance(field, (ManyToOneRel, ManyToManyRel, ManyToManyField))
                        )
                    )
                    for model in models
                ),
                # thesis_thesis:
                # # state:
                # # # created: 'Created'
                # # # published: 'Published'
                table_columns_to_choices=dict(
                    filter(
                        itemgetter(1),
                        (
                            (
                                model._meta.db_table,
                                dict(
                                    (field.column, dict(field.choices))
                                    for field in model._meta.get_fields()
                                    if
                                    not isinstance(field,
                                                   (ManyToOneRel, ManyToManyRel, ManyToManyField)) and field.choices
                                )
                            )
                            for model in models
                        )
                    )
                ),

                # pk mapping to label, only for "safe" models
                # "uuid" -> label
                # "uuid" -> label
                primary_keys_to_labels=dict(
                    (
                        str(obj.pk),
                        str(obj),
                    )
                    for model in map(
                        apps.get_model,
                        settings.AUDIT_REWRITE_PKS_TO_LABELS_FOR_MODELS
                    )
                    for obj in model._base_manager.get_queryset()
                ),

                # thesis_thesis:
                # # state:
                # # # created: 'Created'
                # # # published: 'Published'
                table_columns_to_help_text=dict(
                    filter(
                        itemgetter(1),
                        (
                            (
                                model._meta.db_table,
                                dict(
                                    (field.column, field.help_text)
                                    for field in model._meta.get_fields()
                                    if not isinstance(
                                        field,
                                        (ManyToOneRel, ManyToManyRel, ManyToManyField)
                                    ) and field.help_text
                                )
                            )
                            for model in models
                        )
                    )
                ),

            )
        )
