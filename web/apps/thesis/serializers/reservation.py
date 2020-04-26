from random import choice

from rest_framework.fields import CharField, DateTimeField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.accounts.serializers import UserSerializer
from apps.thesis.models import Reservation


class ReservationSerializer(ModelSerializer):
    for_user = UserSerializer(read_only=True)
    thesis_title = CharField(source='thesis.title')
    thesis_registration_number = CharField(source='thesis.registration_number')
    created = DateTimeField(format="%d.%m.%Y")

    state = SerializerMethodField()

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

    def get_state(self, reservation: Reservation):
        return choice((
            'created',
            'ready',
            'running',
            'finished',
        ))
