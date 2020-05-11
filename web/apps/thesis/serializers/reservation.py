from rest_framework.fields import CharField, CurrentUserDefault
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from apps.thesis.models import Reservation, Thesis


class ReservationSerializer(ModelSerializer):
    thesis = PrimaryKeyRelatedField(
        queryset=Thesis.objects.published(),
    )

    for_user = UserSerializer(read_only=True)
    for_user_id = PrimaryKeyRelatedField(
        write_only=True, source='for_user',
        queryset=User.objects.all(),
        default=CurrentUserDefault(),
    )

    thesis_title = CharField(source='thesis.title', read_only=True)
    thesis_registration_number = CharField(source='thesis.registration_number', read_only=True)

    class Meta:
        model = Reservation
        # TODO: state FSM validation?
        fields = (
            'id',
            'thesis',
            'for_user',
            'for_user_id',
            'thesis_title',
            'thesis_registration_number',
            'created',
            'state',
        )
        read_only_fields = (
            'created',
        )
