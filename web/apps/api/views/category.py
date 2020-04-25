from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.thesis.models import Category
from apps.thesis.serializers.category import CategoryOptionSerializer


class CategoryOptionsViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryOptionSerializer
    pagination_class = None
    search_fields = (
        'title',
    )
