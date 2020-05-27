from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateField, BooleanField, CharField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer, UserInternalSerializer
from apps.attachment.serializers import AttachmentSerializer
from apps.review.serializers import ReviewFullInternalSerializer
from apps.thesis.models import Thesis
from apps.thesis.serializers import CategorySerializer


class ThesisBaseSerializer(ModelSerializer):
    state_label = CharField(source='get_state_display', read_only=True)

    authors = UserSerializer(read_only=True, many=True)

    supervisor = UserSerializer(read_only=True)
    opponent = UserSerializer(read_only=True)

    supervisor_id = PrimaryKeyRelatedField(
        write_only=True, source='supervisor', allow_null=True, required=False,
        queryset=User.school_users.teachers(),
    )
    opponent_id = PrimaryKeyRelatedField(
        write_only=True, source='opponent', allow_null=True, required=False,
        queryset=User.school_users.teachers()
    )

    class Meta:
        model = Thesis
        fields = (
            'id',
            'title',
            'abstract',
            'state',
            'state_label',

            'authors',
            'supervisor',
            'supervisor_id',
            'opponent',
            'opponent_id',
        )

    def validate(self, attrs):
        attrs = super().validate(attrs=attrs)
        if attrs.get('state') == Thesis.State.PUBLISHED and not attrs.get('registration_number'):
            raise ValidationError(_('Publishing thesis without filled registration number is not allowed.'))

        return attrs


class ThesisSubmitSerializer(ThesisBaseSerializer):
    class Meta:
        model = Thesis
        fields = (
            'id',
            'abstract',
            'reservable',
        )


class ThesisFullPublicSerializer(ThesisBaseSerializer):
    category = CategorySerializer(read_only=True)
    published_at = DateField(format="%Y/%m", required=False, read_only=True)
    reservable = BooleanField(read_only=True, source='_reservable')  # set by queryset from viewset

    class Meta:
        model = Thesis
        fields = ThesisBaseSerializer.Meta.fields + (
            'registration_number',
            'published_at',
            'category',

            'available_for_reservation',
            'reservable',
            'open_reservations_count',
        )


class ThesisFullInternalSerializer(ThesisFullPublicSerializer):
    attachments = AttachmentSerializer(many=True, source='attachment_thesis', read_only=True)
    reviews = ReviewFullInternalSerializer(many=True, source='review_thesis', read_only=True)

    supervisor = UserInternalSerializer(read_only=True)
    opponent = UserInternalSerializer(read_only=True)

    class Meta:
        model = Thesis
        fields = ThesisFullPublicSerializer.Meta.fields + (
            'attachments',
            'reviews',
        )
