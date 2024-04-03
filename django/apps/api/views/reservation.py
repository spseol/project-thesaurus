from constance import config
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import CharFilter, FilterSet
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.models import User
from apps.api.permissions import CanCancelReservation
from apps.thesis.models import Reservation, Thesis
from apps.thesis.serializers import ReservationSerializer
from apps.utils.views import ModelChoicesOptionsView


class ReservationFilter(FilterSet):
    state = CharFilter(method='filter_by_state')

    def filter_by_state(self, queryset: QuerySet, field_name, value):
        if value == Reservation.State.OPEN.value:
            return queryset.filter(state__in=Reservation.State.OPEN_RESERVATION_STATES)

        if value in Reservation.State.values:
            return queryset.filter(state=value)

        raise ValidationError(_('Invalid state filter.'), code='invalid_state')

    class Meta:
        model = Reservation
        fields = ('state',)


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.select_related(
        'thesis',
        'user',
    ).prefetch_related(
        'thesis__authors',
    )
    serializer_class = ReservationSerializer
    search_fields = (
        'user__first_name',
        'user__last_name',
        'thesis__title',
        'thesis__registration_number',
    )
    filterset_class = ReservationFilter

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.has_perm('thesis.change_reservation'):
            return qs

        return qs.filter(
            state__in=Reservation.State.OPEN_RESERVATION_STATES
        ).filter(
            user=self.request.user
        )

    def perform_create(self, serializer: ReservationSerializer):
        user = serializer.validated_data.get('user')  # type: User
        thesis = serializer.validated_data.get('thesis')  # type: Thesis

        if Reservation.open_reservations.filter(
                user=user,
                thesis=thesis,
        ).exists():
            raise ValidationError(_('There is already existing reservation for this thesis by user.'))

        if not thesis.reservable:
            raise ValidationError(_('This thesis is not reservable.'))

        if Reservation.open_reservations.filter(
                user=user,
        ).count() >= config.MAX_OPEN_RESERVATIONS_COUNT:
            raise ValidationError(_(
                'Cannot create new reservation, maximum count of opened reservations/borrows is {}.'
            ).format(config.MAX_OPEN_RESERVATIONS_COUNT))

        serializer.save()

    @action(detail=True, methods=['patch'], permission_classes=[CanCancelReservation])
    def cancel(self, request, *args, **kwargs):
        reservation = self.get_object()  # type: Reservation
        serializer = ReservationSerializer(
            instance=reservation,
            data=dict(state=Reservation.State.CANCELED),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class ReservationStateOptionsViewSet(ModelChoicesOptionsView):
    choices = Reservation.State
