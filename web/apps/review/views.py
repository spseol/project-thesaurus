from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin

from apps.review.models import Review


# TODO: perms
class ReviewPdfView(WeasyTemplateResponseMixin, DetailView):
    pdf_attachment = False
    model = Review
    template_name = 'review/review_detail.html'
