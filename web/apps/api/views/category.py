from django.db.models import F
from django.db.models.functions import ExtractYear
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from apps.thesis.models import Category, Thesis
from apps.thesis.serializers.category import CategoryOptionSerializer


class CategoryOptionsViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryOptionSerializer
    pagination_class = None
    search_fields = (
        'title',
    )


class ThesisYearViewSet(GenericViewSet):
    queryset = Thesis.objects.annotate(
        published_at_year=ExtractYear('published_at')
    ).values('published_at_year').distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.values(
            value=F('published_at_year'),
            text=F('published_at_year'),
        ))
