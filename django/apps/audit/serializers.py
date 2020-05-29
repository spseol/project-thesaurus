from typing import Type

from django.apps import apps
from django.db.models import Model
from rest_framework.fields import SerializerMethodField, IntegerField, DateTimeField
from rest_framework.serializers import ModelSerializer

from apps.audit.models import AuditLog
from apps.utils.utils import keydefaultdict

UNIVERSAL_SERIALIZERS = keydefaultdict(
    lambda k: type(  # new model serializer for model `k`
        f'Serializer{k}',
        (ModelSerializer,),
        dict(
            Meta=type(
                f'SerializerMeta{k}',
                (object,),
                dict(
                    model=apps.get_model(k),  # linked to model
                    fields=tuple(
                        filter(  # all attributes except listed
                            lambda attname: attname not in ('id', 'created', 'modified'),
                            map(
                                lambda f: f.attname,
                                apps.get_model(k)._meta.fields
                            )
                        )
                    ),
                )
            ),
            # **{
            #     field.attname: UNIVERSAL_SERIALIZERS[field.remote_field.model.__name__]()
            #     for field in
            #     filter(
            #         lambda f: isinstance(f, ForeignKey) and isinstance(f.remote_field, ForeignObjectRel),
            #         apps.get_model(k)._meta.fields
            #     )
            # }
        )
    )
)


class AuditLogSerializer(ModelSerializer):
    id = IntegerField(source='event_id')
    timestamp = DateTimeField(source='action_tstamp_clk')
    instance = SerializerMethodField()

    @staticmethod
    def get_instance(obj: AuditLog):
        model_name = obj.table_name.replace('_', '.')
        model_pk = obj.row_data.get('id')
        model: Type[Model] = apps.get_model(model_name)
        instance = model._base_manager.get(pk=model_pk)

        return dict(
            **UNIVERSAL_SERIALIZERS[model_name](
                instance=instance
            ).data,
            __str__=str(instance),
        )

    class Meta:
        model = AuditLog
        fields = (
            'id',
            'user',
            'timestamp',
            'instance',
            'changed_fields',
        )
