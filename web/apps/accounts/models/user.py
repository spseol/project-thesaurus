from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from apps.accounts.models.managers import UserQueryset


class User(AbstractUser):
    """Replacement for default Django user with some additional stuff."""

    # TODO: custom fields?

    full_name = property(AbstractUser.get_full_name)

    objects = UserQueryset.as_manager()

    @property
    def is_teacher(self):
        return self.groups.filter(name='teacher').exists()

    @property
    def is_student(self):
        return self.groups.filter(name='student').exists()

    @property
    def is_manager(self):
        return self.groups.filter(name='manager').exists()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
