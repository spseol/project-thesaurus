from rest_framework.fields import CharField, DateTimeField
from rest_framework.serializers import ModelSerializer

from apps.accounts.serializers import UserSerializer
from apps.thesis.models import Reservation


class ReservationSerializer(ModelSerializer):
    for_user = UserSerializer(read_only=True)
    thesis_title = CharField(source='thesis.title')
    thesis_registration_number = CharField(source='thesis.registration_number')
    created = DateTimeField(format="%d.%m.%Y")

    class Meta:
        model = Reservation
        fields = (
            'id',
            'for_user',
            'thesis_title',
            'thesis_registration_number',
            'created',
            'state',
        )
