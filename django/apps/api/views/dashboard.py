from django.db.models import Q
from rest_framework.fields import DateField
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.views import APIView

from apps.thesis.models import Thesis, Reservation
from apps.thesis.serializers import ThesisBaseSerializer, ReservationSerializer


class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)  # handling perms by own (no default)

    def get(self, request: Request):
        user = self.request.user
        theses_ready_for_review = Thesis.objects.filter(
            Q(supervisor=user) | Q(opponent=user),
            state=Thesis.State.READY_FOR_REVIEW,
        ).exclude(review_thesis__user=user)

        reservations_ready_for_prepare = ()
        if self.request.user.has_perm('thesis.change_reservation'):
            reservations_ready_for_prepare = Reservation.objects.filter(
                state=Reservation.State.CREATED,
            )

        theses_just_submitted = ()
        if self.request.user.has_perm('thesis.change_thesis'):
            theses_just_submitted = Thesis.objects.filter(
                state=Thesis.State.SUBMITTED,
            )

        author_theses = Thesis.objects.filter(
            authors=user,
        )
        author_theses_serializer: ListSerializer = ThesisBaseSerializer(
            many=True,
            instance=author_theses
        )
        # dynamically add submit_deadline to standard thesis serializer
        author_theses_serializer.child.fields['submit_deadline'] = DateField()

        return Response(data=dict(
            theses_ready_for_review=ThesisBaseSerializer(
                many=True,
                instance=theses_ready_for_review
            ).data,
            reservations_ready_for_prepare=ReservationSerializer(
                many=True,
                instance=reservations_ready_for_prepare
            ).data,
            theses_just_submitted=ThesisBaseSerializer(
                many=True,
                instance=theses_just_submitted
            ).data,
            author_theses=author_theses_serializer.data,
        ))
