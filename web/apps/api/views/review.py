from rest_framework.viewsets import ModelViewSet

from apps.api.permissions import RestrictedViewModelPermissions
from apps.review.models import Review
from apps.review.serializers import ReviewSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.get_queryset().select_related(
        'thesis__opponent',
        'thesis__supervisor',
    ).prefetch_related(
        'thesis__authors',
    )
    permission_classes = (RestrictedViewModelPermissions,)
    serializer_class = ReviewSerializer
