from typing import Tuple

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Case, Exists, OuterRef, Q, QuerySet, Value, When
from django.shortcuts import get_list_or_404
from django_filters import FilterSet
from django_filters.rest_framework import backends
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework import filters
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.models import User
from apps.api.permissions import (CanSubmitExternalThesisReviewPermission, CanSubmitThesisPermission, CanViewAttachment,
                                  CanViewThesisFullInternalReview)
from apps.api.utils.filters import InListFilter, InMultipleFieldsListFilter
from apps.api.utils.pagination import DynamicPageSizePagination
from apps.attachment.models import Attachment, TypeAttachment
from apps.attachment.serializers import AttachmentSerializer
from apps.review.serializers import ReviewFullInternalSerializer, ReviewPublicSerializer
from apps.thesis.models import Category, Reservation, Thesis
from apps.thesis.serializers import (ThesisFullInternalSerializer, ThesisFullPublicSerializer, ThesisSubmitSerializer)
from apps.utils.utils import parse_date
from apps.utils.views import ModelChoicesOptionsView


def _state_change_action(name, state: Thesis.State):
    def _action_method(self: 'ThesisViewSet', request: Request, *args, **kwargs):
        thesis = self.get_object()  # type: Thesis
        self.get_serializer()
        serializer = self.get_serializer(instance=thesis, data=dict(state=state), partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    _action_method.__name__ = name

    return transaction.atomic(
        action(methods=['patch'], detail=True)(_action_method)
    )


class ThesisFilterSet(FilterSet):
    category = InListFilter(field_name='category__id', label='Category ID (comma separated)')
    year = InListFilter(field_name='published_at_year', label='Year of publication (comma separated)')
    teacher = InMultipleFieldsListFilter(
        label='Username of related teacher (comma separated)',
        field_name='supervisor__username opponent__username'
    )


class ThesisViewSet(ModelViewSet):
    queryset = Thesis.api_objects.get_queryset()
    pagination_class = DynamicPageSizePagination

    filter_backends = [
        filters.SearchFilter,
        backends.DjangoFilterBackend
    ]
    filterset_class = ThesisFilterSet

    search_fields = (
        'title__unaccent',
        'abstract__unaccent',
        'registration_number',
        'state',
        '=authors__username',
        'authors__first_name__unaccent',
        'authors__last_name__unaccent',

        '=supervisor__username',
        '=opponent__username',
    )

    def get_queryset(self):
        qs = super().get_queryset()  # type: QuerySet
        user = self.request.user  # type: User

        qs = qs.annotate(
            already_has_reservation=Exists(
                queryset=Reservation.open_reservations.filter(
                    thesis_id=OuterRef('pk'),
                    user=user,
                ),
            )
        ).annotate(
            _reservable=Case(
                When(
                    Q(reservable=True, already_has_reservation=False),
                    then=Value(True)
                ),
                default=Value(False)
            )
        )

        # no perms to see all thesis, so filter only published ones
        if not user.has_perm('thesis.change_thesis'):
            qs = qs.filter(
                Q(state=Thesis.State.PUBLISHED) |
                Q(authors=user) |
                Q(opponent=user, state=Thesis.State.READY_FOR_REVIEW) |
                Q(supervisor=user, state=Thesis.State.READY_FOR_REVIEW)
            )

        return qs

    @transaction.atomic
    def perform_create(self, serializer: ThesisFullPublicSerializer):
        thesis = serializer.save(
            category=get_object_or_404(Category, pk=serializer.initial_data.get('category')),
            supervisor=serializer.validated_data.get('supervisor'),
            authors=get_list_or_404(
                get_user_model(),
                pk__in=serializer.initial_data.get('authors').split(',')
            ),
            published_at=parse_date((serializer.initial_data.get('published_at') + '/01').replace('/', '-'))
        )

        admission = self.request.FILES.get('admission')
        if admission:
            Attachment.objects.create_from_upload(
                uploaded=admission,
                thesis=thesis,
                type_attachment=TypeAttachment.objects.get_by_identifier(TypeAttachment.Identifier.THESIS_ASSIGMENT),
            )

        thesis.state = Thesis.State.READY_FOR_SUBMIT
        thesis.save()

    @transaction.atomic
    def perform_update(self, serializer: ThesisFullInternalSerializer):
        data = dict()
        if author_pks := serializer.initial_data.get('authors'):
            data['authors'] = get_list_or_404(
                get_user_model(),
                pk__in=author_pks
            )
        if published_at := serializer.initial_data.get('published_at'):
            data['published_at'] = parse_date((published_at + '/01').replace('/', '-'))

        serializer.save(**data)

    @action(methods=['patch'], detail=True, permission_classes=[CanSubmitThesisPermission])
    @transaction.atomic
    def submit(self, request: Request, *args, **kwargs):
        serializer = ThesisSubmitSerializer(
            instance=self.get_object(),
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        thesis = serializer.save(
            state=Thesis.State.SUBMITTED,
        )
        Attachment.objects.create_from_upload(
            uploaded=request.FILES.get('thesisText'),
            thesis=thesis,
            type_attachment=TypeAttachment.objects.get_by_identifier(TypeAttachment.Identifier.THESIS_TEXT),
        )

        if poster := request.FILES.get('thesisPoster'):
            Attachment.objects.create_from_upload(
                uploaded=poster,
                thesis=thesis,
                type_attachment=TypeAttachment.objects.get_by_identifier(TypeAttachment.Identifier.THESIS_POSTER),
            )
        if attachment := request.FILES.get('thesisAttachment'):
            Attachment.objects.create_from_upload(
                uploaded=attachment,
                thesis=thesis,
                type_attachment=TypeAttachment.objects.get_by_identifier(TypeAttachment.Identifier.THESIS_ATTACHMENT),
            )

        return Response(data=serializer.data)

    send_to_submit = _state_change_action('send_to_submit', Thesis.State.READY_FOR_SUBMIT)
    send_to_review = _state_change_action('send_to_review', Thesis.State.READY_FOR_REVIEW)
    publish = _state_change_action('publish', Thesis.State.PUBLISHED)

    @action(methods=['post'], detail=True, permission_classes=[CanSubmitExternalThesisReviewPermission])
    @transaction.atomic
    def submit_external_review(self, request: Request, *args, **kwargs):
        thesis = self.get_object()

        review_type_attachment = TypeAttachment.IDENTIFIER_BY_REVIEWER.get(request.data.get('reviewer'))

        review_file = request.FILES.get('review')
        if not (review_type_attachment and review_file):
            raise ValidationError()

        Attachment.objects.create_from_upload(
            uploaded=review_file,
            thesis=thesis,
            type_attachment=TypeAttachment.objects.get_by_identifier(review_type_attachment),
        )

        return Response(data=self.get_serializer(instance=thesis).data)

    @action(methods=['get'], detail=True)
    def reviews(self, request, *args, **kwargs):
        thesis = self.get_object()

        serializer_class = ReviewPublicSerializer
        if CanViewThesisFullInternalReview().has_object_permission(self.request, self, thesis):
            serializer_class = ReviewFullInternalSerializer

        return Response(
            serializer_class(
                instance=thesis.review_thesis, many=True, context=self.get_serializer_context()
            ).data
        )

    @action(methods=['get'], detail=True)
    def attachments(self, request, *args, **kwargs):
        thesis = self.get_object()

        return Response(
            AttachmentSerializer(
                instance=CanViewAttachment.restrict_queryset(
                    user=request.user,
                    queryset=thesis.attachment_thesis
                ),
                many=True,
                context=self.get_serializer_context()
            ).data
        )

    def get_serializer_class(self):
        class DynamicThesisSerializer(ThesisFullInternalSerializer):
            class Meta:
                model = Thesis
                # skip ThesisFullInternalSerializer to avoid variant fields attachments and reviews
                fields = ThesisFullPublicSerializer.Meta.fields + tuple(filter(None, (
                    'attachments' if self.request.user.has_perm('attachment.view_attachment') else None,
                    'reviews' if self.request.user.has_perm('review.view_review') else None,
                )))

        return DynamicThesisSerializer


class ThesisStateOptionsViewSet(ModelChoicesOptionsView):
    choices = Thesis.State

    @staticmethod
    def choice_extra(choice: Tuple[str, str]):
        return dict(
            help_text=Thesis.STATE_HELP_TEXTS.get(choice[0]),
        )
