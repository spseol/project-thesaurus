from rest_framework.serializers import ModelSerializer

from apps.accounts.serializers import UserSerializer
from apps.thesis.models import Thesis


class ThesisSerializer(ModelSerializer):
    author = UserSerializer()
    supervisor = UserSerializer()
    opponent = UserSerializer()

    class Meta:
        model = Thesis
        fields = (
            'id',
            'title',
            'registration_number',
            'author',
            'supervisor',
            'opponent',
        )
