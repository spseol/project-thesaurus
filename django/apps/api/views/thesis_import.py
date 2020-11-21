from typing import Optional

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http import HttpRequest
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from apps.thesis.models import Thesis
from apps.thesis.serializers import ThesisBaseSerializer
from apps.utils.utils import parse_date


class ThesisImportViewSet(GenericViewSet):
    queryset = Thesis.api_objects.all()
    serializer_class = ThesisBaseSerializer

    def initialize_request(self, request: HttpRequest, *args, **kwargs):
        request.upload_handlers = [TemporaryFileUploadHandler(request=request)]
        return super().initialize_request(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        to_import: Optional[TemporaryUploadedFile] = request.FILES.get('import')
        published_at = parse_date((request.data.get('published_at') + '/01').replace('/', '-'))
        if not (to_import and published_at):
            return Response(
                data=dict(
                    error=True,
                    message=_('Missing some of needed arguments.'),
                    success=False,
                ),
                status=HTTP_400_BAD_REQUEST,
            )

        return Thesis.import_objects.import_from_file(
            file_to_import=to_import,
            published_at=published_at,
            is_final_import=request.data.get('final') == str(True).lower()
        )

    @action(detail=False)
    def columns(self, request):
        asdict = lambda col: {k: getattr(col, k) for k in 'title description icon'.split(' ')}
        return Response(
            data=dict(
                file_examples=dict(
                    csv=static('thesis/import-example.csv'),
                    xlsx=static('thesis/import-example.xlsx'),
                ),
                columns=tuple(
                    map(
                        asdict,
                        Thesis.import_objects.columns_definition
                    )
                )
            )
        )
