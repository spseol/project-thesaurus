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
        'author__id',
        'author__first_name',
        'author__last_name',
        'supervisor__id',
        'supervisor__first_name',
        'supervisor__last_name',
        'opponent__id',
        'opponent__first_name',
        'opponent__last_name',
        'category__title',
        # TODO: fix filtering by date
        # TODO: https://stackoverflow.com/questions/33358120/django-rest-framework-month-and-year-as-numberfilter
        # 'published_at__year',
        # 'published_at__month',
    )
