from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from apps.accounts.models import User
from apps.thesis.models import Reservation, Thesis
from apps.thesis.serializers import ReservationSerializer
from apps.utils.views import ModelChoicesOptionsView


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.select_related(
        'thesis',
        'for_user',
    )
    serializer_class = ReservationSerializer
    pagination_class = None  # TODO: needed pagination?
    search_fields = (
        'for_user__first_name',
        'for_user__last_name',
        'thesis__title',
        'thesis__registration_number',
    )

    def perform_create(self, serializer: ReservationSerializer):
        user = serializer.validated_data.get('for_user')  # type: User
        thesis = serializer.validated_data.get('thesis')  # type: Thesis

        if Reservation.open_reservations.filter(
                for_user=user,
                thesis=thesis,
        ).exists():
            raise ValidationError(_('There is already existing reservation for this thesis by user.'))

        # TODO: check also limit for borrowed theses per user

        serializer.save()


class ReservationStateOptionsViewSet(ModelChoicesOptionsView):
    choices = Reservation.State
