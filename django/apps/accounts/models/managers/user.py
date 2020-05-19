from __future__ import annotations

from django.db.models import QuerySet


class UserQueryset(QuerySet):
    def with_school_account(self) -> __qualname__:
        return self.teachers() | self.students()

    def teachers(self) -> __qualname__:
        return self.filter(groups__name='teacher')

    def students(self) -> __qualname__:
        return self.filter(groups__name='student')
