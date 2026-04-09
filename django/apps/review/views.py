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

    def get_queryset(self):
        return super().get_queryset().select_related('thesis__category')

    def has_permission(self):
        review: Review = self.get_object()

        return CanViewThesisFullInternalReview().has_object_permission(
            request=self.request,
            view=self,
            thesis=review.thesis,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.get_object()
        grades_choices = review.get_grades_choices()
        context['grades_choices'] = grades_choices
        context['grade_proposal_display'] = grades_choices(review.grade_proposal).label
        difficulty_choices = review.get_difficulty_choices()
        context['difficulty_choices'] = difficulty_choices
        context['difficulty_display'] = difficulty_choices(review.difficulty).label
        return context
