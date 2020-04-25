from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.accounts.serializers import UserOptionSerializer


class UserOptionsViewSet(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    # TODO: exclude admins
    queryset = get_user_model().objects.all()
    pagination_class = None
    serializer_class = UserOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )


class StudentOptionsViewSet(ReadOnlyModelViewSet):
    # TODO: not so public please
    permission_classes = [permissions.IsAuthenticated]
    # TODO: include only students
    queryset = get_user_model().objects.all()
    pagination_class = None
    serializer_class = UserOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )


class TeacherOptionsViewSet(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    # TODO: include only teachers
    queryset = get_user_model().objects.all()
    pagination_class = None
    serializer_class = UserOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )
