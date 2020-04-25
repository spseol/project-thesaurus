from rest_framework.fields import DateField
from rest_framework.serializers import ModelSerializer

from apps.accounts.serializers import UserSerializer
from apps.thesis.models import Thesis
from apps.thesis.serializers import CategorySerializer


class ThesisSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    supervisor = UserSerializer(read_only=True)
    opponent = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    published_at = DateField(format="%Y/%m", required=False, read_only=True)

    class Meta:
        model = Thesis
        fields = (
            'id',
            'title',
            'registration_number',
            'published_at',
            'category',
            'author',
            'supervisor',
            'opponent',
        )
