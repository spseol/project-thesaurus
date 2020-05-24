from rest_framework.fields import CharField, CurrentUserDefault
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from apps.thesis.models import Reservation, Thesis


class ReservationSerializer(ModelSerializer):
    thesis = PrimaryKeyRelatedField(
        queryset=Thesis.objects.published(),
        style=dict(base_template='input.html'),
    )

    user = UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(
        write_only=True, source='user',
        queryset=User.objects.all(),
        default=CurrentUserDefault(),
        style=dict(base_template='input.html'),
    )

    thesis_label = CharField(source='thesis.__str__', read_only=True)
    thesis_registration_number = CharField(source='thesis.registration_number', read_only=True)
    state_label = CharField(source='get_state_display', read_only=True)

    class Meta:
        model = Reservation
        # TODO: state FSM validation?
        fields = (
            'id',
            'thesis',
            'user',
            'user_id',
            'thesis_label',
            'thesis_registration_number',
            'created',
            'state',
            'state_label',
        )

        read_only_fields = (
            'created',
        )
