from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin

from apps.api.permissions import CanViewThesisFullInternalReview
from apps.review.models import Review


# class ReviewPdfView(PermissionRequiredMixin, DetailView):
class ReviewPdfView(WeasyTemplateResponseMixin, PermissionRequiredMixin, DetailView):
    pdf_attachment = False
    model = Review
    template_name = 'review/review_detail.html'

    def has_permission(self):
        review: Review = self.get_object()

        return CanViewThesisFullInternalReview().has_object_permission(
            request=self.request,
            view=self,
            thesis=review.thesis,
        )
