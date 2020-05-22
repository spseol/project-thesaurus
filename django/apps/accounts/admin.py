from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as OldUserAdmin
from django.utils.translation import ugettext_lazy as _

from apps.accounts.models import User


@register(User)
class UserAdmin(OldUserAdmin):
    change_form_template = 'loginas/change_form.html'
    list_display = ('username', 'full_name', 'school_class', 'get_groups', 'is_active')
    list_filter = OldUserAdmin.list_filter + ('school_class',)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.prefetch_related('groups')

    def get_groups(self, user: User):
        return ', '.join(map(str, user.groups.all()))

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('degree_before', 'first_name', 'last_name', 'degree_after', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
