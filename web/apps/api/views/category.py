from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.thesis.models import Category
from apps.thesis.serializers import CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = (
        'title',
    )
