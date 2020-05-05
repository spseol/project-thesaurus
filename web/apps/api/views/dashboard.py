from django.db.models import Q
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.thesis.models import Thesis
from apps.thesis.serializers import ThesisBaseSerializer


class DashboardView(APIView):
    def get(self, request: Request):
        user = self.request.user
        theses_ready_for_submit = Thesis.objects.filter(
            authors=user,
            state=Thesis.State.READY_FOR_SUBMIT,
        )
        theses_ready_for_review = Thesis.objects.filter(
            Q(supervisor=user) | Q(opponent=user),
            Q(review_thesis__user=user, _negated=True),
            state=Thesis.State.READY_FOR_REVIEW,
        )

        # TODO: theses waiting for physical submit
        # TODO: theses waiting for reservation pickup

        return Response(data=dict(
            theses_ready_for_submit=ThesisBaseSerializer(many=True, instance=theses_ready_for_submit).data,
            theses_ready_for_review=ThesisBaseSerializer(many=True, instance=theses_ready_for_review).data,
        ))
