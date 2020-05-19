from rest_framework.permissions import DjangoModelPermissions, BasePermission

from apps.accounts.models import User
from apps.thesis.models import Thesis, Reservation


class RestrictedViewModelPermissions(DjangoModelPermissions):
    """
    Same as parent, but requires also app.view_model perm for retrieve/list.
    """
    perms_map = {
        **DjangoModelPermissions.perms_map,
        'GET': ['%(app_label)s.view_%(model_name)s'],
    }


class CanSubmitThesisPermission(BasePermission):
    def has_object_permission(self, request, view, thesis: Thesis):
        user = request.user  # type: User

        return user in thesis.authors.get_queryset() and thesis.state == Thesis.State.READY_FOR_SUBMIT


class CanSubmitExternalThesisReviewPermission(BasePermission):
    def has_object_permission(self, request, view, thesis: Thesis):
        user = request.user  # type: User

        return user.has_perms(
            ('review.add_review', 'attachment.add_attachment')
        ) and thesis.state == Thesis.State.READY_FOR_REVIEW


class CanCancelReservation(BasePermission):
    def has_object_permission(self, request, view, reservation: Reservation):
        user = request.user  # type: User

        return user.has_perm('thesis.change_reservation') or (
                reservation.for_user == user and reservation.state ==
                Reservation.State.CREATED
        )
