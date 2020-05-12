from rest_framework.viewsets import ModelViewSet

from apps.thesis.models import Reservation
from apps.thesis.serializers import ReservationSerializer


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.select_related(
        'thesis',
        'for_user',
    )
    # permission_classes = (RestrictedViewModelPermissions,)
    serializer_class = ReservationSerializer
    pagination_class = None  # TODO: needed pagination?
    search_fields = (
        'for_user__first_name',
        'for_user__last_name',
        'thesis__title',
        'thesis__registration_number',
    )
