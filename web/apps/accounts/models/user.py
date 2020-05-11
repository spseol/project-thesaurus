from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import CharField
from django.utils.translation import gettext as _

from apps.accounts.models.managers import UserQueryset


class User(AbstractUser):
    """Replacement for default Django user with some additional stuff."""

    # TODO: custom fields? class?

    degree_before = CharField(
        verbose_name=_('Degree before'),
        null=True, blank=True, max_length=16,
    )
    degree_after = CharField(
        verbose_name=_('Degree after'),
        null=True, blank=True, max_length=16,
    )

    objects = UserManager()
    school_users = UserQueryset.as_manager()

    @property
    def is_teacher(self):
        return self.groups.filter(name='teacher').exists()

    @property
    def is_student(self):
        return self.groups.filter(name='student').exists()

    @property
    def is_manager(self):
        return self.groups.filter(name='manager').exists()

    def get_full_name(self):
        return f'{self.degree_before or ""}' \
               f'{self.first_name} {self.last_name}' \
               f'{("," + self.degree_after) if self.degree_after else ""}'.strip()

    full_name = property(get_full_name)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
