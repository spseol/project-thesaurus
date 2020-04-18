from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as OldUserAdmin

from apps.accounts.models import User


@register(User)
class UserAdmin(OldUserAdmin):
    pass
