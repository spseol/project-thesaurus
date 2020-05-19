from django.db import models
from django.db.models import Q, OuterRef, Subquery
from rest_framework.fields import IntegerField
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from apps.thesis.models import Thesis


class SQLCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = models.IntegerField()


class ThesesCompetitionViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.get_queryset().annotate(
        theses_count=SQLCount(
            Thesis.objects.published().filter(
                Q(supervisor=OuterRef('pk'))
                |
                Q(opponent=OuterRef('pk'))
            )  # .exclude(category__title__in=('SL', 'EL'))
        )
    ).order_by('-theses_count').filter(theses_count__gt=1)
    pagination_class = None

    class serializer_class(UserSerializer):
        theses_count = IntegerField(read_only=True)

        class Meta(UserSerializer.Meta):
            fields = UserSerializer.Meta.fields + (
                'theses_count',
            )
