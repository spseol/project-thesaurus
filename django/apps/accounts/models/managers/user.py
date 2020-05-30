from __future__ import annotations

import typing
from typing import Optional

from django.contrib.auth.models import UserManager as AuthUserManager
from django.db.models import QuerySet
from django.utils.text import slugify

if typing.TYPE_CHECKING:
    from apps.accounts.models import User


class UserQueryset(QuerySet):
    def with_school_account(self) -> __qualname__:
        return self.teachers() | self.students()

    def teachers(self) -> __qualname__:
        return self.filter(groups__name='teacher')

    def students(self) -> __qualname__:
        return self.filter(groups__name='student')


class UserManager(AuthUserManager):
    @staticmethod
    def get_or_create_from_name(*, name: str, thesis_id: Optional[str]) -> Optional['User']:
        from apps.accounts.models import User

        name = name.replace('.', '. ').strip()

        if name.strip() == '-':
            return None

        degree_after = None
        if ',' in name:
            name, degree_after = name.rsplit(',', 1)

        [last_name, *degrees_before] = tuple(filter(None, name.strip().rsplit(' ', 2)[::-1]))

        first_name = degrees_before[0] if degrees_before else ''

        if thesis_id:
            # is student
            username = f'{last_name.strip()[:3].ljust(3, "0")}{thesis_id:05}'
        else:
            username = last_name.strip()

        username = slugify(username.strip().lower())

        if User.objects.filter(username=username).exists():
            pass  # username = f'{username}.{thesis_id}'

        return User.objects.get_or_create(
            username=username,
            defaults=dict(
                last_name=last_name.strip(),
                first_name=first_name.strip(),
                degree_after=degree_after or None,
                degree_before=''.join(degrees_before[1:]).replace(' ', '').replace('.', '. ') or None,
                is_active=False,  # activation by ldap sync
            ),
        )
