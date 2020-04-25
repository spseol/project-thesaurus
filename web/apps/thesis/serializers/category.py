from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from apps.thesis.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
        )


class CategoryOptionSerializer(ModelSerializer):
    value = CharField(source='id')
    text = CharField(source='title')

    class Meta:
        model = Category
        fields = (
            'id',
            'value',
            'text',
        )
