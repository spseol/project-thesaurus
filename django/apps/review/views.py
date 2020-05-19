from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin

from apps.review.models import Review


class ReviewPdfView(WeasyTemplateResponseMixin, PermissionRequiredMixin, DetailView):
    pdf_attachment = False
    model = Review
    template_name = 'review/review_detail.html'
    permission_required = ('review.view_review',)
