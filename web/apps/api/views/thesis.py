from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404
from django.utils.dateparse import parse_date
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from apps.thesis.models import Thesis, Category
from apps.thesis.serializers import ThesisSerializer


# TODO: needed ModelViewSet?
class ThesisViewSet(ModelViewSet):
    queryset = Thesis.objects.all().select_related('supervisor', 'opponent').prefetch_related('authors')
    serializer_class = ThesisSerializer
    search_fields = (
        'title',
        'abstract',
        'registration_number',
        'authors__username',
        'authors__first_name',
        'authors__last_name',
        'supervisor__username',
        'supervisor__first_name',
        'supervisor__last_name',
        'opponent__username',
        'opponent__first_name',
        'opponent__last_name',
        'category__id',
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
            authors=get_list_or_404(
                get_user_model(),
                pk__in=serializer.initial_data.get('authors').split(',')
            ),
            published_at=parse_date((serializer.initial_data.get('published_at') + '/01').replace('/', '-'))
        )
