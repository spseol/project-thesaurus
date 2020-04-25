from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from apps.thesis.models import Thesis, Category
from apps.thesis.serializers import ThesisSerializer


# TODO: needed ModelViewSet?
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

    def perform_create(self, serializer: ThesisSerializer):
        # TODO: save attachment
        self.request.FILES.get('admission')

        instance = serializer.save(
            category=get_object_or_404(Category, pk=serializer.initial_data.get('category')),
            supervisor=get_object_or_404(get_user_model(), pk=serializer.initial_data.get('supervisor')),
            author=get_object_or_404(get_user_model(), pk=serializer.initial_data.get('authors')[0]),
            published_at=parse_date(serializer.initial_data.get('published_at') + '-01')
        )
