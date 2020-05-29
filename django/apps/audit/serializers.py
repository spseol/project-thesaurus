from django.apps import apps
from rest_framework.fields import SerializerMethodField, IntegerField, DateTimeField, CharField
from rest_framework.serializers import ModelSerializer

from apps.accounts.serializers import UserSerializer
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
    action_label = CharField(source='get_action_display')
    user = UserSerializer()

    __model__ = CharField(source='table_name')
    __str__ = SerializerMethodField()

    table_name_to_verbose_name = keydefaultdict(lambda k: apps.get_model(k)._meta.verbose_name)

    class Meta:
        model = AuditLog
        fields = (
            'id',
            'action',
            'action_label',
            'user',
            'timestamp',
            'row_data',
            'changed_fields',
            '__model__',
            '__str__',
        )

    @classmethod
    def get___str__(cls, obj: AuditLog):
        return cls.table_name_to_verbose_name[obj.model_name]
