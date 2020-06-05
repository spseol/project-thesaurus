from django.db.models import Count, QuerySet
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from django_filters import FilterSet
from django_filters.rest_framework import BooleanFilter
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.accounts.models import User
from apps.accounts.serializers import UserOptionSerializer, StudentOptionSerializer


class UserFilterOptionsViewSet(ReadOnlyModelViewSet):
    queryset = User.school_users.with_school_account().teachers().annotate(
        thesis_count=Count('thesis_supervisor') + Count('thesis_opponent')
    ).order_by('-thesis_count')
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    serializer_class = UserOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )


class StudentFilter(FilterSet):
    only_active = BooleanFilter(method='filter_active', label=_('Include only active users'))

    def filter_active(self, queryset: QuerySet, field_name, value: bool):
        if value:
            return queryset.filter(is_active=True)
        return queryset

    class Meta:
        model = User
        fields = ('only_active',)


class StudentOptionsViewSet(ReadOnlyModelViewSet):
    queryset = User.school_users.students()
    pagination_class = None
    serializer_class = StudentOptionSerializer
    search_fields = (
        'first_name',
        'last_name',
    )
    filterset_class = StudentFilter


class TeacherOptionsViewSet(ReadOnlyModelViewSet):
    queryset = User.school_users.teachers().annotate(
        thesis_count=Count('thesis_supervisor') + Count('thesis_opponent')
    ).order_by('-thesis_count')
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
        # multiple perms?
        return Response(request.user.has_perm(perm))
