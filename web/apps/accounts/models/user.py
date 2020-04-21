from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


class User(AbstractUser):
    """Replacement for default Django user with some additional stuff."""

    # TODO: custom fields?

    full_name = property(AbstractUser.get_full_name)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
