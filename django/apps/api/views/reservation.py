from constance import config
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.models import User
from apps.api.permissions import CanCancelReservation
from apps.thesis.models import Reservation, Thesis
from apps.thesis.serializers import ReservationSerializer
from apps.utils.views import ModelChoicesOptionsView


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.select_related(
        'thesis',
        'for_user',
    ).prefetch_related(
        'thesis__authors',
    )
    serializer_class = ReservationSerializer
    pagination_class = None  # TODO: needed pagination?
    search_fields = (
        'for_user__first_name',
        'for_user__last_name',
        'thesis__title',
        'thesis__registration_number',
    )

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.has_perm('thesis.change_reservation'):
            return qs

        return qs.filter(
            state__in=Reservation.OPEN_RESERVATION_STATES
        ).filter(
            for_user=self.request.user
        )

    def perform_create(self, serializer: ReservationSerializer):
        user = serializer.validated_data.get('for_user')  # type: User
        thesis = serializer.validated_data.get('thesis')  # type: Thesis

        if Reservation.open_reservations.filter(
                for_user=user,
                thesis=thesis,
        ).exists():
            raise ValidationError(_('There is already existing reservation for this thesis by user.'))

        if Reservation.open_reservations.filter(
                for_user=user,
        ).count() + 1 > config.MAX_OPEN_RESERVATIONS_COUNT:
            raise ValidationError(
                _('Cannot create new reservation, maximum count of opened reservations/borrows is {}.').format(
                    config.MAX_OPEN_RESERVATIONS_COUNT)
            )

        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[CanCancelReservation])
    def cancel(self, request, *args, **kwargs):
        reservation = self.get_object()  # type: Reservation
        serializer = ReservationSerializer(
            instance=reservation, data=dict(state=Reservation.State.CANCELED),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class ReservationStateOptionsViewSet(ModelChoicesOptionsView):
    choices = Reservation.State
