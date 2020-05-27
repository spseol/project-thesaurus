from django.contrib.admin import ModelAdmin, register, StackedInline

from apps.thesis.models import Thesis, Reservation, Category, ThesisAuthor


class AuthorInline(StackedInline):
    model = Thesis.authors.through


@register(Thesis)
class ThesisAdmin(ModelAdmin):
    list_display = (
        '__str__',
        'supervisor',
        'opponent',
        'category',
        'registration_number',
        'published_at',
        'state',
        'reservable',
    )
    search_fields = (
        'title',
        'abstract',
    )

    date_hierarchy = 'published_at'

    list_filter = (
        'state',
        'category',
        'authors__school_class',
    )

    autocomplete_fields = ('supervisor', 'opponent',)

    inlines = (AuthorInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('authors').select_related('category', 'supervisor', 'opponent')


@register(ThesisAuthor)
class ThesisAuthorAdmin(ModelAdmin):
    pass


@register(Reservation)
class ReservationAdmin(ModelAdmin):
    pass


@register(Category)
class CategoryAdmin(ModelAdmin):
    pass
