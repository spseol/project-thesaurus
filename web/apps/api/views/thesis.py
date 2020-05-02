from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q, QuerySet
from django.shortcuts import get_list_or_404
from django.utils.dateparse import parse_date
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from apps.accounts.models import User
from apps.api.permissions import RestrictedViewModelPermissions
from apps.attachment.models import Attachment, TypeAttachment
from apps.thesis.models import Thesis, Category
from apps.thesis.serializers import ThesisFullSerializer


# TODO: needed ModelViewSet?
class ThesisViewSet(ModelViewSet):
    queryset = Thesis.api_objects.get_queryset()
    serializer_class = ThesisFullSerializer
    permission_classes = (RestrictedViewModelPermissions,)
    search_fields = (
        'title',
        'abstract',
        'registration_number',
        'state',
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

    def get_queryset(self):
        qs = super().get_queryset()  # type: QuerySet
        user = self.request.user  # type: User

        # in case of request for one object include also thesis waiting for submit by one author
        include_waiting_for_submit = self.action == 'retrieve'

        if user.has_perm('thesis.change_thesis'):
            return qs

        # no perms to see all thesis, so filter only published ones
        return qs.filter(
            Q(state=Thesis.State.PUBLISHED) |
            Q(authors=user, state=Thesis.State.READY_FOR_SUBMIT) if include_waiting_for_submit else Q()
        )

    @transaction.atomic
    def perform_create(self, serializer: ThesisFullSerializer):
        thesis = serializer.save(
            category=get_object_or_404(Category, pk=serializer.initial_data.get('category')),
            supervisor=get_object_or_404(get_user_model(), pk=serializer.initial_data.get('supervisor')),
            authors=get_list_or_404(
                get_user_model(),
                pk__in=serializer.initial_data.get('authors').split(',')
            ),
            published_at=parse_date((serializer.initial_data.get('published_at') + '/01').replace('/', '-'))
        )

        Attachment.objects.create_from_upload(
            uploaded=self.request.FILES.get('admission'),
            thesis=thesis,
            type_attachment=TypeAttachment.objects.get_by_identifier(TypeAttachment.Identifier.THESIS_ASSIGMENT),
        )

        thesis.state = Thesis.State.READY_FOR_SUBMIT
        thesis.save()
