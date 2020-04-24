from rest_framework.serializers import ModelSerializer

from apps.thesis.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
        )
