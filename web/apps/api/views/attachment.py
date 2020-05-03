import logging

from drf_pdf.renderer import PDFRenderer
from drf_pdf.response import PDFResponse
from rest_framework import status
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.attachment.models import Attachment
from apps.attachment.models.managers import default_storage


class AttachmentViewSet(GenericViewSet):
    renderer_classes = (PDFRenderer, StaticHTMLRenderer)
    queryset = Attachment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # type: Attachment

        if not default_storage.exists(instance.file_path):
            logging.error('Attachment file not found on storage.')
            return Response('Attachment not found.', status=status.HTTP_404_NOT_FOUND)

        attachment = default_storage.open(instance.file_path).read()

        return PDFResponse(
            attachment,
            instance.public_file_name.rsplit('.', 1)[0],
            status=status.HTTP_200_OK,
        )
