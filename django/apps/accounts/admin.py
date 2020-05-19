from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as OldUserAdmin

from apps.accounts.models import User


@register(User)
class UserAdmin(OldUserAdmin):
    change_form_template = 'loginas/change_form.html'
    list_display = ('username', 'full_name', 'get_groups')

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.prefetch_related('groups')

    def get_groups(self, user: User):
        return ', '.join(map(str, user.groups.all()))
