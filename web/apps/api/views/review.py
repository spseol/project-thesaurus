from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from apps.api.permissions import RestrictedViewModelPermissions
from apps.review.models import Review
from apps.review.serializers import ReviewSerializer
from apps.thesis.models import Thesis


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.get_queryset()
    permission_classes = (RestrictedViewModelPermissions,)
    serializer_class = ReviewSerializer

    @transaction.atomic
    def perform_create(self, serializer: ReviewSerializer):
        thesis = get_object_or_404(Thesis, pk=serializer.initial_data.get('thesis', dict()).get('id'))
        user = self.request.user

        if not (
                thesis.state == Thesis.State.READY_FOR_REVIEW and
                user in (thesis.supervisor, thesis.opponent) and
                not Review.objects.filter(thesis=thesis, user=user).exists()
        ):
            raise PermissionDenied(_('Creating review for this thesis is not allowed in this case.'))

        review = serializer.save(
            user=user,
            thesis=thesis,
        )

        review.save()
