from django.contrib.admin import register, TabularInline
from django.contrib.auth.admin import UserAdmin as OldUserAdmin
from django.db.models.functions import Length
from django.utils.translation import ugettext_lazy as _

from apps.accounts.models import User
from apps.review.models import Review
from apps.thesis.models import Thesis, ThesisAuthor


class RelatedThesisInline(TabularInline):
    can_delete = False
    model = Thesis
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    has_add_permission = has_change_permission
    has_delete_permission = has_change_permission


class ThesisInlineSupervisorInline(RelatedThesisInline):
    fk_name = 'supervisor'
    verbose_name = _('Supervised thesis')
    verbose_name_plural = _('Supervised theses')


class ThesisInlineOpponentInline(RelatedThesisInline):
    fk_name = 'opponent'
    verbose_name = _('Opponented thesis')
    verbose_name_plural = _('Opponented theses')


class AuthorInlineOpponentInline(RelatedThesisInline):
    model = ThesisAuthor
    verbose_name = _('Author of thesis')
    verbose_name_plural = _('Author of theses')


class ReviewInline(RelatedThesisInline):
    model = Review
    verbose_name = _('Author of review')
    verbose_name_plural = _('Author of reviews')


@register(User)
class UserAdmin(OldUserAdmin):
    change_form_template = 'loginas/change_form.html'
    list_display = ('username', 'full_name', 'school_class', 'groups_labels', 'is_active', 'username_length')
    list_filter = OldUserAdmin.list_filter + ('school_class',)
    save_on_top = True

    inlines = [ThesisInlineSupervisorInline, ThesisInlineOpponentInline, AuthorInlineOpponentInline, ReviewInline]

    def username_length(self, obj):
        return obj.username_length

    username_length.admin_order_field = 'username_length'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).annotate(username_length=Length('username'))
        return qs.prefetch_related(
            'groups',
            'thesis_supervisor',
            'thesis_supervisor__authors',
            'thesis_opponent',
            'thesis_opponent__authors',
            'review_user',
            'review_user__thesis',
            'thesis_author_author',
            'thesis_author_author__author',
        ).order_by('username_length')

    def groups_labels(self, user: User):
        return ', '.join(map(str, user.groups.all()))

    groups_labels.short_description = _('Groups')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('degree_before', 'first_name', 'last_name',
                                         'degree_after', 'email', 'school_class')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
