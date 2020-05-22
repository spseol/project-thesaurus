from django.db.models import Count
from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.accounts.models import User
from apps.accounts.models.managers import UserQueryset
from apps.accounts.serializers import UserOptionSerializer, StudentOptionSerializer


class UserFilterOptionsViewSet(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    serializer_class = UserOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )

    def get_queryset(self):
        queryset = User.school_users.with_school_account().teachers()  # type: UserQueryset

        queryset = queryset.annotate(
            thesis_count=Count('thesis_supervisor') + Count('thesis_opponent')
        ).order_by('-thesis_count')
        # TODO: add students for role>=teacher?
        if self.request.user.is_teacher or self.request.user.is_manager or self.request.user.is_superuser:
            return queryset

        return queryset.teachers()


class StudentOptionsViewSet(ReadOnlyModelViewSet):
    queryset = User.school_users.students()
    pagination_class = None
    serializer_class = StudentOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )


class TeacherOptionsViewSet(ReadOnlyModelViewSet):
    queryset = User.school_users.teachers()
    pagination_class = None
    serializer_class = UserOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )


class UserPermView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get(self, request: HttpRequest, perm: str):
        return Response(request.user.has_perm(perm))
