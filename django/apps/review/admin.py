from django.contrib.admin import ModelAdmin, register

from apps.review.models import Review


@register(Review)
class ReviewAdmin(ModelAdmin):
    pass
