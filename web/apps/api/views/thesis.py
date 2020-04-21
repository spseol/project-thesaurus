from rest_framework.viewsets import ModelViewSet

from apps.thesis.models import Thesis
from apps.thesis.serializers import ThesisSerializer


class ThesisViewSet(ModelViewSet):
    queryset = Thesis.objects.all().select_related('author', 'supervisor', 'opponent')
    serializer_class = ThesisSerializer
