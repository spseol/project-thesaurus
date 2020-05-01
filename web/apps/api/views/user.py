from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.accounts.models import User
from apps.accounts.models.managers import UserQueryset
from apps.accounts.serializers import UserOptionSerializer


class UserFilterOptionsViewSet(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    serializer_class = UserOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )

    def get_queryset(self):
        queryset = User.objects.with_school_account()  # type: UserQueryset

        if self.request.user.is_teacher or self.request.user.is_manager:
            return queryset

        return queryset.teachers()


class StudentOptionsViewSet(ReadOnlyModelViewSet):
    # TODO: not so public please
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.students()
    pagination_class = None
    serializer_class = UserOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )


class TeacherOptionsViewSet(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.teachers()
    pagination_class = None
    serializer_class = UserOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )
