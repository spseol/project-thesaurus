from django.contrib.admin import ModelAdmin, register, TabularInline

from apps.thesis.models import Thesis, Reservation, Category, ThesisAuthor


class AuthorInline(TabularInline):
    model = ThesisAuthor
    extra = 1


@register(Thesis)
class ThesisAdmin(ModelAdmin):
    search_fields = (
        'title',
        'abstract',
    )

    # inlines = (AuthorInline, )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('authors')


@register(ThesisAuthor)
class ThesisAuthorAdmin(ModelAdmin):
    pass


@register(Reservation)
class ReservationAdmin(ModelAdmin):
    pass


@register(Category)
class CategoryAdmin(ModelAdmin):
    pass
