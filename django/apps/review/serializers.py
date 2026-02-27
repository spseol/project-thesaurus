from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateTimeField, CurrentUserDefault, HiddenField
from rest_framework.relations import PrimaryKeyRelatedField, HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from apps.accounts.serializers import UserSerializer
from apps.review.models import Review
from apps.thesis.models import Thesis


class ReviewPublicSerializer(ModelSerializer):
    thesis = PrimaryKeyRelatedField(
        queryset=Thesis.objects.get_queryset(),
        style=dict(base_template='input.html'),
    )
    user = UserSerializer(read_only=True)
    user_id = HiddenField(default=CurrentUserDefault(), source='user', write_only=True)

    url = HyperlinkedIdentityField(view_name='api:review-pdf-detail')

    created = DateTimeField(read_only=True, format=None)

    class Meta:
        model = Review
        fields = (
            'id',
            'url',
            'thesis',
            'user',
            'user_id',
            'difficulty',
            'grades',
            'grade_proposal',
            'created',
        )

    def validate(self, attrs):
        thesis = attrs.get('thesis')
        user = self.context.get('request').user if not self.instance else self.instance.user

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

        choices_class, max_value, _ = Review.get_grade_config(
            thesis.category.grade_type, thesis.published_at
        )
        valid_values = set(choices_class.values)

        for g in attrs.get('grades', []):
            if g not in valid_values:
                raise ValidationError(
                    _('Invalid grade value %(value)s. Allowed values: %(allowed)s.')
                    % {'value': g, 'allowed': ', '.join(str(v) for v in sorted(valid_values))}
                )

        grade_proposal = attrs.get('grade_proposal')
        if grade_proposal is not None and grade_proposal not in valid_values:
            raise ValidationError(
                _('Invalid grade proposal value %(value)s. Allowed values: %(allowed)s.')
                % {'value': grade_proposal, 'allowed': ', '.join(str(v) for v in sorted(valid_values))}
            )

        return attrs


class ReviewFullInternalSerializer(ReviewPublicSerializer):
    class Meta(ReviewPublicSerializer.Meta):
        fields = ReviewPublicSerializer.Meta.fields + (
            'comment',
            'questions',
        )
