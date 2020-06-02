import logging

from rest_framework import status
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from apps.api.permissions import CanViewAttachment
from apps.attachment.models import Attachment, TypeAttachment
from apps.attachment.models.managers import default_storage
from apps.attachment.serializers import TypeAttachmentFullSerializer, AttachmentSerializer


class AttachmentViewSet(DestroyModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Attachment.objects.all()
    permission_classes = (CanViewAttachment,)
    serializer_class = AttachmentSerializer

    def retrieve(self, request, *args, **kwargs):
        attachment = self.get_object()  # type: Attachment

        if not default_storage.exists(attachment.file_path):
            logging.error('Attachment file not found on storage.')
            return Response('Attachment not found.', status=status.HTTP_404_NOT_FOUND)

        return Response(
            headers={
                'X-Accel-Redirect': default_storage.url(attachment.file_path),
                'Content-Disposition': f'filename="{attachment.public_file_name}"',
            },
            content_type=attachment.content_type,
            status=status.HTTP_200_OK,
        )

    def perform_create(self, serializer: AttachmentSerializer):
        serializer.instance = Attachment.objects.create_from_upload(
            uploaded=self.request.FILES.get('file'),
            thesis=serializer.validated_data.get('thesis'),
            type_attachment=serializer.validated_data.get('type_attachment'),
        )


class TypeAttachmentViewSet(ReadOnlyModelViewSet):
    queryset = TypeAttachment.objects.all()
    serializer_class = TypeAttachmentFullSerializer
    pagination_class = None
