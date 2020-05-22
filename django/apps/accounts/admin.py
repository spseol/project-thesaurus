from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as OldUserAdmin
from django.db.models.functions import Length
from django.utils.translation import ugettext_lazy as _

from apps.accounts.models import User


@register(User)
class UserAdmin(OldUserAdmin):
    change_form_template = 'loginas/change_form.html'
    list_display = ('username', 'full_name', 'school_class', 'groups_labels', 'is_active', 'username_length')
    list_filter = OldUserAdmin.list_filter + ('school_class',)

    def username_length(self, obj):
        return obj.username_length

    username_length.admin_order_field = 'username_length'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).annotate(username_length=Length('username'))
        return qs.prefetch_related('groups').order_by('username_length')

    def groups_labels(self, user: User):
        return ', '.join(map(str, user.groups.all()))

    groups_labels.short_description = _('Groups')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('degree_before', 'first_name', 'last_name', 'degree_after', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
