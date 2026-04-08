from django.contrib.admin import ModelAdmin, register, RelatedOnlyFieldListFilter
from django.utils.translation import gettext_lazy as _

from apps.review.models import Review


@register(Review)
class ReviewAdmin(ModelAdmin):
    date_hierarchy = "thesis__published_at"
    list_display = ["thesis", "user", "created", "grade_proposal_display"]

    list_filter = (
        ("user", RelatedOnlyFieldListFilter),
        "grade_proposal",
    )

    @staticmethod
    def grade_proposal_display(obj: Review) -> str:
        choices_class = obj.get_grades_choices()
        try:
            return choices_class(obj.grade_proposal).label
        except ValueError:
            return str(obj.grade_proposal)

    grade_proposal_display.short_description = _("Proposed grade")
