from rest_framework.fields import DateField, BooleanField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from apps.attachment.serializers import AttachmentSerializer
from apps.review.serializers import ReviewSerializer
from apps.thesis.models import Thesis
from apps.thesis.serializers import CategorySerializer


class ThesisBaseSerializer(ModelSerializer):
    authors = UserSerializer(read_only=True, many=True)

    supervisor = UserSerializer(read_only=True)
    opponent = UserSerializer(read_only=True)

    supervisor_id = PrimaryKeyRelatedField(
        write_only=True, source='supervisor', allow_null=True,
        queryset=User.school_users.teachers(),
    )
    opponent_id = PrimaryKeyRelatedField(
        write_only=True, source='opponent', required=False,
        queryset=User.school_users.teachers()
    )

    class Meta:
        model = Thesis
        fields = (
            'id',
            'title',
            'abstract',
            'state',

            'authors',
            'supervisor',
            'supervisor_id',
            'opponent',
            'opponent_id',
        )


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
    reviews = ReviewSerializer(many=True, source='review_thesis', read_only=True)

    class Meta:
        model = Thesis
        fields = ThesisFullPublicSerializer.Meta.fields + (
            'attachments',
            'reviews',
        )
