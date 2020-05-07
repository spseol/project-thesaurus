from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.accounts.serializers import UserSerializer
from apps.review.models import Review
from apps.thesis.models import Thesis


class ReviewSerializer(ModelSerializer):
    thesis = PrimaryKeyRelatedField(queryset=Thesis.objects.get_queryset())
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

    def validate(self, attrs):
        thesis = attrs.get('thesis')
        user = self.context['request'].user if not self.instance else self.instance.user

        if not (
                thesis.state == Thesis.State.READY_FOR_REVIEW and
                user in (thesis.supervisor, thesis.opponent) and
                not Review.objects.filter(
                    thesis=thesis,
                    user=user
                ).exclude(
                    id=self.instance.id if self.instance else None
                ).exists()
        ):
            raise ValidationError(_('Review has been already posted by this user or this user is not allowed to post '
                                    'review for this thesis.'))

        return attrs
