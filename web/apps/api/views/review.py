from django.db import transaction
from rest_framework.viewsets import ModelViewSet

from apps.api.permissions import RestrictedViewModelPermissions
from apps.review.models import Review
from apps.review.serializers import ReviewSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.get_queryset()
    permission_classes = (RestrictedViewModelPermissions,)
    serializer_class = ReviewSerializer

    @transaction.atomic
    def perform_create(self, serializer: ReviewSerializer):
        serializer.save(
            user=self.request.user,  # TODO: Current user default?
        )
    # TODO: perform update?
