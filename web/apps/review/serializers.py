from rest_framework.serializers import ModelSerializer

from apps.accounts.serializers import UserSerializer
from apps.review.models import Review
from apps.thesis.serializers import ThesisBaseSerializer


class ReviewSerializer(ModelSerializer):
    thesis = ThesisBaseSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'thesis',
            'user',
            'comment',
            'questions',
            'difficulty',
            'grades',
            'grade_proposal',
        )
