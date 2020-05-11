from django.contrib.admin import ModelAdmin, register

from apps.thesis.models import Thesis, Reservation, Category, ThesisAuthor


@register(Thesis)
class ThesisAdmin(ModelAdmin):
    pass


@register(ThesisAuthor)
class ThesisAuthorAdmin(ModelAdmin):
    pass


@register(Reservation)
class ReservationAdmin(ModelAdmin):
    pass


@register(Category)
class CategoryAdmin(ModelAdmin):
    pass
