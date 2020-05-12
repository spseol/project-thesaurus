from rest_framework.fields import CharField
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


class UserOptionSerializer(UserSerializer):
    value = CharField(source='id')
    text = CharField(source='full_name')

    class Meta(UserSerializer.Meta):
        fields = (
            'username',
            'value',
            'text',
        )
