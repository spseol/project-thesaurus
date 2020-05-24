import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.attachment.models import Attachment
from apps.attachment.models.managers import default_storage


class AttachmentViewSet(GenericViewSet):
    queryset = Attachment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        attachment = self.get_object()  # type: Attachment

        # TODO: check t_a.is_public

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
