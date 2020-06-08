from django.contrib.admin import ModelAdmin, register, RelatedOnlyFieldListFilter

from apps.review.models import Review


@register(Review)
class ReviewAdmin(ModelAdmin):
    date_hierarchy = 'thesis__published_at'
    list_display = ['thesis', 'user', 'created', 'grade_proposal']

    list_filter = (
        ('user', RelatedOnlyFieldListFilter),
        'grade_proposal',
    )
