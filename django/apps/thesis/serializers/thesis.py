from rest_framework.fields import BooleanField, CharField, DateField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.accounts.models import User
from apps.accounts.serializers import UserInternalSerializer, UserSerializer
from apps.attachment.serializers import AttachmentSerializer
from apps.review.serializers import ReviewFullInternalSerializer
from apps.thesis.models import Category, Thesis
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


class ThesisSubmitSerializer(ThesisBaseSerializer):
    class Meta:
        model = Thesis
        fields = (
            'id',
            'abstract',
            'reservable',
        )
        extra_kwargs = {'abstract': {'required': True, 'allow_blank': False, 'allow_null': False}}


class ThesisFullPublicSerializer(ThesisBaseSerializer):
    category = CategorySerializer(read_only=True)
    category_id = PrimaryKeyRelatedField(
        write_only=True, source='category', allow_null=True, required=False,
        queryset=Category.objects.all(),
    )
    published_at = DateField(format="%Y/%m", required=False, read_only=True)
    reservable = BooleanField(read_only=True, source='_reservable')  # set by queryset from viewset

    submit_deadline = DateField(required=False, allow_null=True)

    class Meta:
        model = Thesis
        fields = ThesisBaseSerializer.Meta.fields + (
            'registration_number',
            'published_at',
            'category',
            'category_id',

            'available_for_reservation',
            'reservable',
            'open_reservations_count',
            'submit_deadline',
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
