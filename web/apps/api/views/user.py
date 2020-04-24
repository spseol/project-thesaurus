from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.accounts.serializers import UserOptionSerializer


class UserOptionsViewSet(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()
    pagination_class = None
    serializer_class = UserOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )
