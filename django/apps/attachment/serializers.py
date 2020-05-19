from rest_framework.fields import CharField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from apps.attachment.models import Attachment, TypeAttachment


class TypeAttachmentSerializer(ModelSerializer):
    name = CharField(source='get_identifier_display')

    class Meta:
        model = TypeAttachment
        fields = (
            'name',
            'identifier',
        )
        read_only_fields = fields


class AttachmentSerializer(ModelSerializer):
    type_attachment = TypeAttachmentSerializer()

    url = HyperlinkedIdentityField(view_name='api:v1:attachment-detail')

    class Meta:
        model = Attachment
        fields = (
            'id',
            'type_attachment',
            'url',
            'content_type',
        )

        read_only_fields = fields
