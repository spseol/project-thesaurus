from django.db.models import Q
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.thesis.models import Thesis, Reservation
from apps.thesis.serializers import ThesisBaseSerializer, ReservationSerializer


class DashboardView(APIView):
    def get(self, request: Request):
        user = self.request.user
        theses_ready_for_submit = Thesis.objects.filter(
            authors=user,
            state=Thesis.State.READY_FOR_SUBMIT,
        )
        theses_ready_for_review = Thesis.objects.filter(
            Q(supervisor=user) | Q(opponent=user),
            state=Thesis.State.READY_FOR_REVIEW,
        ).exclude(review_thesis__user=user)
        reservations_ready_for_prepare = Reservation.objects.filter(
            state=Reservation.State.CREATED,
        )

        # TODO: theses waiting for physical submit

        return Response(data=dict(
            theses_ready_for_submit=ThesisBaseSerializer(many=True, instance=theses_ready_for_submit).data,
            theses_ready_for_review=ThesisBaseSerializer(many=True, instance=theses_ready_for_review).data,
            reservations_ready_for_prepare=ReservationSerializer(many=True,
                                                                 instance=reservations_ready_for_prepare).data,
        ))
