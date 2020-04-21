from rest_framework.serializers import ModelSerializer

from apps.accounts.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'full_name',
        )
