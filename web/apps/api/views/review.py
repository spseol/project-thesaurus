from django.db import transaction
from rest_framework.viewsets import ModelViewSet

from apps.api.permissions import RestrictedViewModelPermissions
from apps.review.models import Review
from apps.review.serializers import ReviewSubmitSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.get_queryset()
    permission_classes = (RestrictedViewModelPermissions,)
    serializer_class = ReviewSubmitSerializer

    @transaction.atomic
    def perform_create(self, serializer: ReviewSubmitSerializer):
        review = serializer.save(
            user=self.request.user,
            thesis=serializer.validated_data.get('thesis_id')
        )

        review.save()

    # TODO: perform update?
