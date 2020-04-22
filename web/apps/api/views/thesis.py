from rest_framework.viewsets import ModelViewSet

from apps.thesis.models import Thesis
from apps.thesis.serializers import ThesisSerializer


class ThesisViewSet(ModelViewSet):
    queryset = Thesis.objects.all().select_related('author', 'supervisor', 'opponent')
    serializer_class = ThesisSerializer
    search_fields = (
        'title',
        'abstract',
        'registration_number',
        'author__first_name',
        'author__last_name',
        'supervisor__first_name',
        'supervisor__last_name',
        'opponent__first_name',
        'opponent__last_name',
    )
