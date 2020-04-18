from django.contrib.admin import ModelAdmin, register

from apps.thesis.models import Thesis, Reservation, Category


@register(Thesis)
class ThesisAdmin(ModelAdmin):
    pass


@register(Reservation)
class ReservationAdmin(ModelAdmin):
    pass


@register(Category)
class CategoryAdmin(ModelAdmin):
    pass
