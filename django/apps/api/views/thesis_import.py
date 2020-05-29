import csv
from dataclasses import dataclass
from io import StringIO
from operator import attrgetter, methodcaller
from typing import Callable, Any

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from apps.accounts.models import User
from apps.thesis.models import Thesis, Category, ThesisAuthor
from apps.thesis.serializers import ThesisBaseSerializer
from apps.utils.utils import parse_date


@dataclass
class Column:
    title: str
    description: str
    icon: str
    resolver: Callable[[Thesis, Any], Any]


class ThesisImportViewSet(GenericViewSet):
    queryset = Thesis.api_objects.all()
    serializer_class = ThesisBaseSerializer

    @property
    def columns_definition(self):
        categories = '/'.join(Category.objects.values_list('title', flat=True))

        return [
            Column(
                _('Student'),
                _('In a format of her/his login (abc12345), split by comma if multiple authors'),
                'school',
                self._set_authors,
            ),
            Column(
                _('Category'),
                _('Two letter abbr of category ({})').format(categories),
                'filter-outline',
                self._set_category,
            ),
            Column(
                _('Title'),
                _('Thesis long title'),
                'format-title',
                self._set_title
            ),
            Column(
                _('Supervisor'),
                _('Login for internal, full name for external'),
                'account-circle',
                self._set_supervisor,
            ),
            Column(
                _('Opponent'),
                _('Login for internal, full name for external'),
                'account-circle',
                self._set_opponent,
            ),
            Column(
                _('Deadline'),
                _('Submit deadline, DD.MM.YYYY'),
                'calendar',
                self._set_submit_deadline,
            ),
        ]

    def _line_to_dict(self, line):
        return {
            col.resolver.__name__[5:]: (part or '')
            for col, part in zip(self.columns_definition, line)
        }

    @staticmethod
    def _prepare_store_value(thesis, data):
        def _store_value(fnc):
            try:
                value = dict(
                    value=str(
                        fnc(thesis, data.get(fnc.__name__[5:]) or '')
                    )
                )
            except ValidationError as e:
                value = dict(
                    value=str(e.message or ''),
                    error=True
                )
            return value

        return _store_value

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        to_import = request.FILES.get('import')
        published_at = parse_date((request.data.get('published_at') + '/01').replace('/', '-'))
        if not (to_import and published_at):
            return Response(
                data=dict(
                    error=True,
                    message=_('Missing some of needed arguments.'),
                    success=False,
                ),
                status=HTTP_400_BAD_REQUEST,
            )

        statuses = []
        content = to_import.file.read().decode('utf-8')
        data = csv.reader(StringIO(content), dialect='excel', )

        sid = transaction.savepoint()

        for line in data:
            thesis = Thesis(published_at=published_at)
            line_status = []

            data = self._line_to_dict(line=line)
            _store_value = self._prepare_store_value(thesis=thesis, data=data)

            line_status.extend((
                _store_value(self._set_category),
                _store_value(self._set_title),
                _store_value(self._set_supervisor),
                _store_value(self._set_opponent),
                _store_value(self._set_submit_deadline),
            ))
            try:
                thesis.full_clean(exclude=('registration_number', 'published_at'))
            except ValidationError as e:
                line_status.append(dict(
                    value='',  # .join(e.error_dict.values()),
                    error=True,
                ))
            else:
                line_status.append(dict(
                    success=True,
                ))

            if not any(s.get('error') for s in line_status):
                thesis.save()
                line_status.insert(0, _store_value(self._set_authors))
            else:
                line_status.insert(0, dict())

            statuses.append(dict(
                statuses=line_status,
                error=any(map(methodcaller('get', 'error'), line_status)),
            ))

        has_error = any(map(methodcaller('get', 'error'), statuses))

        if request.data.get('final') == str(True).lower() and not has_error:
            transaction.savepoint_commit(sid)
            message = _('Theses have been imported.')
        else:
            transaction.savepoint_rollback(sid)
            message = _('Cannot import theses containing errors.')

        return Response(data=dict(
            statuses=statuses,
            error=has_error,
            message=message,
            success=not has_error,
        ), status=HTTP_400_BAD_REQUEST if has_error else HTTP_201_CREATED)

    @action(detail=False)
    def columns(self, request):
        asdict = lambda col: {k: getattr(col, k) for k in 'title description icon'.split(' ')}
        return Response(
            data=tuple(
                map(
                    asdict,
                    self.columns_definition
                )
            )
        )

    def _set_authors(self, thesis: Thesis, authors: str):
        authors_keys = tuple(map(str.strip, authors.split(',')))
        authors: QuerySet = User.school_users.students().filter(username__in=authors_keys)

        if not authors.exists():
            raise ValidationError(_('Unknown author/s.'))
        elif len(authors_keys) != authors.count():
            raise ValidationError(_('Some of authors not found ({}).').format(
                ''.join(tuple(set(authors_keys) - set(authors.values_list('username', flat=True))))
            ))

        for a in authors:
            ThesisAuthor.objects.create(thesis=thesis, author=a)
        return ', '.join(map(attrgetter('full_name'), authors))

    def _set_category(self, thesis: Thesis, category_code: str):
        category = Category.objects.filter(title__iexact=category_code.strip()).first()
        if not category:
            raise ValidationError(_('Unknown category code {}.').format(category_code))
        thesis.category = category
        return thesis.category

    def _set_title(self, thesis: Thesis, title: str):
        thesis.title = title
        if not thesis.title:
            raise ValidationError(_('Empty title.'))
        return title

    def _set_supervisor(self, thesis: Thesis, supervisor: str):
        thesis.supervisor = self._load_reviewer(reviewer=supervisor)
        return thesis.supervisor.full_name + (
            ' (E)' if not thesis.supervisor.is_active else ''
        ) if thesis.supervisor else None

    def _set_opponent(self, thesis: Thesis, opponent: str):
        thesis.opponent = self._load_reviewer(reviewer=opponent)
        return thesis.opponent.full_name + (
            ' (E)' if not thesis.opponent.is_active else ''
        ) if thesis.opponent else None

    def _set_submit_deadline(self, thesis: Thesis, submit_deadline: str):
        thesis.submit_deadline = parse_date(submit_deadline)
        return thesis.submit_deadline

    def _load_reviewer(self, reviewer: str):
        if ' ' not in reviewer:
            # probably username, internal
            user = User.school_users.teachers().filter(username=reviewer).first()
            if not user:
                raise ValidationError(_('Unknown user {}').format(reviewer))
            return user

        # external
        user = User.objects.get_or_create_from_name(name=reviewer, thesis_id=None)[0]
        # TODO: needed?
        user.groups.add(Group.objects.get_or_create(name='teacher')[0])

        return user
