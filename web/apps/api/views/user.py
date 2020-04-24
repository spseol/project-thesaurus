from django.contrib.auth import get_user_model
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.accounts.serializers import UserSerializer


class TeacherViewSet(ReadOnlyModelViewSet):
    queryset = get_user_model().objects.filter(groups__name__in=('teacher',))
    serializer_class = UserSerializer
    search_fields = (
        'first_name',
        'last_name',
    )
