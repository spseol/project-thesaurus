from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q, QuerySet, OuterRef, Exists, F
from django.shortcuts import get_list_or_404
from django.utils.dateparse import parse_date
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.models import User
from apps.api.permissions import CanSubmitThesisPermission, CanSubmitExternalThesisReviewPermission
from apps.attachment.models import Attachment, TypeAttachment
from apps.thesis.models import Thesis, Category, Reservation
from apps.thesis.serializers import ThesisFullPublicSerializer, ThesisFullInternalSerializer, ThesisBaseSerializer
from apps.thesis.serializers.thesis import ThesisSubmitSerializer


def _state_change_action(name, state: Thesis.State):
    # TODO: simple FSM validation?
    def _action_method(self, request: Request, *args, **kwargs):
        thesis = self.get_object()  # type: Thesis
        serializer = ThesisBaseSerializer(instance=thesis, data=dict(state=state), partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    _action_method.__name__ = name

    return transaction.atomic(
        action(methods=['patch'], detail=True)(
            _action_method
        )
    )


class ThesisViewSet(ModelViewSet):
    queryset = Thesis.api_objects.get_queryset()
    search_fields = (
        'title',
        'abstract',
        'registration_number',
        'state',
        '=authors__username',
        'authors__first_name',
        'authors__last_name',
        'supervisor__username',
        'supervisor__first_name',
        'supervisor__last_name',
        'opponent__username',
        'opponent__first_name',
        'opponent__last_name',
        '=category__id',
        'category__title',
        '=published_at_year',
    )

    def get_queryset(self):
        qs = super().get_queryset()  # type: QuerySet
        user = self.request.user  # type: User

        qs = qs.annotate(
            _reservable=F('reservable') and Exists(
                queryset=Reservation.open_reservations.filter(
                    thesis_id=OuterRef('pk'),
                    for_user=user,
                ),
                negated=True,
            )
        )

        # in case of request for one object include also thesis waiting for submit by one author
        include_waiting_for_submit = self.action in ('retrieve', 'submit')

        if user.has_perm('thesis.change_thesis'):  # can see all of them
            return qs

        # no perms to see all thesis, so filter only published ones
        return qs.filter(
            Q(state=Thesis.State.PUBLISHED) |
            (Q(authors=user, state=Thesis.State.READY_FOR_SUBMIT) if include_waiting_for_submit else Q()) |
            Q(opponent=user, state=Thesis.State.READY_FOR_REVIEW) |
            Q(supervisor=user, state=Thesis.State.READY_FOR_REVIEW)
        )

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

        Attachment.objects.create_from_upload(
            uploaded=self.request.FILES.get('admission'),
            thesis=thesis,
            type_attachment=TypeAttachment.objects.get_by_identifier(TypeAttachment.Identifier.THESIS_ASSIGMENT),
        )

        thesis.state = Thesis.State.READY_FOR_SUBMIT
        thesis.save()

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

        attachment = Attachment.objects.create_from_upload(
            uploaded=review_file,
            thesis=thesis,
            type_attachment=TypeAttachment.objects.get_by_identifier(review_type_attachment),
        )

        thesis.check_reviews_state()

        return Response(data=dict(id=attachment.id))

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
