from rest_framework.fields import CharField, IntegerField
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


class UserInternalSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'is_active',
        )


class UserOptionSerializer(UserSerializer):
    value = IntegerField(source='id')
    text = CharField(source='full_name')

    class Meta(UserSerializer.Meta):
        fields = (
            'username',
            'value',
            'text',
        )


class StudentOptionSerializer(UserOptionSerializer):
    text = CharField(source='full_student_name')
