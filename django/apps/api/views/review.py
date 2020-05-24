from rest_framework.viewsets import ModelViewSet

from apps.review.models import Review
from apps.review.serializers import ReviewFullInternalSerializer, ReviewPublicSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.get_queryset().select_related(
        'thesis__opponent',
        'thesis__supervisor',
    ).prefetch_related(
        'thesis__authors',
    )

    def get_serializer_class(self):
        if self.request.user.has_perm('review.add_review'):
            return ReviewFullInternalSerializer

        if self.detail:
            review: Review = self.get_object()
            if self.request.user in review.thesis.authors.all():
                return ReviewFullInternalSerializer

        return ReviewPublicSerializer
