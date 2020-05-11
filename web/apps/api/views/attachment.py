import logging

from drf_pdf.renderer import PDFRenderer
from drf_pdf.response import PDFResponse
from filetype.types.archive import Pdf
from rest_framework import status
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.api.renderers import JpegRenderer, PngRenderer
from apps.attachment.models import Attachment
from apps.attachment.models.managers import default_storage


class AttachmentViewSet(GenericViewSet):
    renderer_classes = (JpegRenderer, PngRenderer, PDFRenderer, StaticHTMLRenderer)
    queryset = Attachment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # type: Attachment

        if not default_storage.exists(instance.file_path):
            logging.error('Attachment file not found on storage.')
            return Response('Attachment not found.', status=status.HTTP_404_NOT_FOUND)

        attachment_content = default_storage.open(instance.file_path).read()

        extension = instance.get_content_type_display()

        # TODO: nginx x-file serve?
        if extension == Pdf.EXTENSION:
            return PDFResponse(
                attachment_content,
                instance.public_file_name.rsplit('.', 1)[0],
                status=status.HTTP_200_OK,
            )

        return Response(
            data=attachment_content,
            status=status.HTTP_200_OK,
            content_type=instance.content_type,
        )
