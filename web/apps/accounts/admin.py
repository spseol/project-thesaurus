from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as OldUserAdmin

from apps.accounts.models import User


@register(User)
class UserAdmin(OldUserAdmin):
    change_form_template = 'loginas/change_form.html'
    pass
