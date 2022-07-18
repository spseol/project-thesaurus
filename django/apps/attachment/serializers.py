from rest_framework.fields import CharField, ListField
from rest_framework.relations import HyperlinkedIdentityField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.attachment.models import Attachment, TypeAttachment
from apps.thesis.models import Thesis


class TypeAttachmentSerializer(ModelSerializer):
    name = CharField(source='get_identifier_display')
    max_size_label = CharField()
    allowed_content_types_extensions = ListField(child=CharField())

    class Meta:
        model = TypeAttachment
        fields = (
            'name',
            'identifier',
            'max_size',
            'max_size_label',
            'allowed_content_types_extensions',
        )
        read_only_fields = fields


class AttachmentSerializer(ModelSerializer):
    type_attachment = TypeAttachmentSerializer(read_only=True)
    type_attachment_id = PrimaryKeyRelatedField(
        write_only=True, source='type_attachment',
        queryset=TypeAttachment.objects.all(),
    )

    thesis_id = PrimaryKeyRelatedField(
        write_only=True, source='thesis',
        queryset=Thesis.objects.all(),
    )

    url = HyperlinkedIdentityField(view_name='api:v1:attachment-detail')

    class Meta:
        model = Attachment
        fields = (
            'id',
            'type_attachment',
            'type_attachment_id',
            'url',
            'content_type',
            'size_label',
            'thesis_id',
        )
        read_only_fields = ('content_type',)


class TypeAttachmentFullSerializer(TypeAttachmentSerializer):
    class Meta(TypeAttachmentSerializer.Meta):
        fields = TypeAttachmentSerializer.Meta.fields + (
            'id',
            'allowed_content_types',
            'max_size',
        )
        read_only_fields = fields
