import csv
from dataclasses import dataclass
from datetime import datetime
from io import StringIO
from operator import methodcaller, attrgetter
from typing import Any, TYPE_CHECKING, Callable, List, Dict, Union

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db import transaction
from django.db.models import QuerySet, Manager
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from openpyxl import load_workbook, Workbook
from openpyxl.utils.exceptions import InvalidFileException
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from apps.utils.utils import parse_date

if TYPE_CHECKING:
    from apps.thesis.models import Thesis


@dataclass
class Column:
    title: str
    description: str
    icon: str
    resolver: Callable[['Thesis', Any], Any]


class ThesisImportManager(Manager):
    def _load_csv(self, file_to_import):
        content = file_to_import.file.read()
        try:
            content = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                content = content.decode('cp1250')
            except UnicodeDecodeError as e:
                return Response(data=dict(
                    error=True,
                    message=_('Unable to parse file to import: {}.').format(e),
                    success=False,
                ), status=HTTP_400_BAD_REQUEST)

        data_file = StringIO(content)

        try:
            dialect = csv.Sniffer().sniff(data_file.read(1024))
            data_file.seek(0)
        except csv.Error as e:
            return Response(data=dict(
                error=True,
                message=_('Unable to detect CSV format: {}.').format(e),
                success=False,
            ), status=HTTP_400_BAD_REQUEST)

        return csv.reader(data_file, dialect=dialect)

    def _load_xls(self, wb: Workbook):
        return list(wb.active.values)

    @transaction.atomic
    def import_from_file(self, file_to_import: TemporaryUploadedFile, published_at: datetime.date,
                         is_final_import: bool):
        sid = transaction.savepoint()

        try:
            wb = load_workbook(file_to_import.temporary_file_path(), read_only=True, data_only=True, )

            data_or_response = self._load_xls(wb=wb)
        except InvalidFileException as e:
            data_or_response = self._load_csv(file_to_import)

        if isinstance(data_or_response, HttpResponse):
            return data_or_response

        statuses = []

        for line in data_or_response:
            thesis = self.model(published_at=published_at)
            line_status: List[Dict[str, Any]] = []

            data_or_response = self._line_to_dict(line=line)
            _store_value = self._prepare_store_value(thesis=thesis, data=data_or_response)

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
                    value=', '.join(map(lambda t: f'{t[0]}: {t[1]}', e.error_dict.items())),
                    error=True,
                ))
            else:
                line_status.append(dict(
                    success=True,
                ))

            line_has_error = any(map(methodcaller('get', 'error'), line_status))
            if not line_has_error:
                thesis.save()
                line_status.insert(0, _store_value(self._set_authors))
            else:
                line_status.insert(0, dict())

            statuses.append(dict(
                statuses=line_status,
                error=line_has_error or line_status[0].get('error'),
            ))

        has_error = any(map(methodcaller('get', 'error'), statuses))

        if is_final_import and not has_error:
            transaction.savepoint_commit(sid)
            message = _('Theses have been imported.')
        else:
            transaction.savepoint_rollback(sid)
            message = _('Cannot import theses containing errors.')

        return Response(data=dict(
            statuses=statuses,
            error=has_error,
            message=message,
            success=True,
        ), status=HTTP_400_BAD_REQUEST if has_error else HTTP_201_CREATED)

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
                        fnc(thesis, data.get(fnc.__name__[5:]) or '') or ''
                    )
                )
            except ValidationError as e:
                value = dict(
                    value=str(e.message or ''),
                    error=True
                )
            return value

        return _store_value

    def _set_authors(self, thesis: 'Thesis', authors: str):
        from apps.accounts.models import User
        from apps.thesis.models import ThesisAuthor

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

    def _set_category(self, thesis: 'Thesis', category_code: str):
        from apps.thesis.models import Category

        category = Category.objects.filter(title__iexact=category_code.strip()).first()
        if not category:
            raise ValidationError(_('Unknown category code {}.').format(category_code))
        thesis.category = category
        return thesis.category

    def _set_title(self, thesis: 'Thesis', title: str):
        thesis.title = title.strip()
        if not thesis.title:
            raise ValidationError(_('Empty title.'))

        same_title = self.filter(title=thesis.title)
        if same_title.exists():
            raise ValidationError(_('Found thesis with same name: {}.').format(
                ' ,'.join(map(str, same_title))
            ))
        return thesis.title

    def _set_supervisor(self, thesis: 'Thesis', supervisor: str):
        thesis.supervisor = self._load_reviewer(reviewer=supervisor)
        return thesis.supervisor.full_name + (
            ' (E)' if not thesis.supervisor.is_active else ''
        ) if thesis.supervisor else None

    def _set_opponent(self, thesis: 'Thesis', opponent: str):
        thesis.opponent = self._load_reviewer(reviewer=opponent)
        return thesis.opponent.full_name + (
            ' (E)' if not thesis.opponent.is_active else ''
        ) if thesis.opponent else None

    def _set_submit_deadline(self, thesis: 'Thesis', submit_deadline: Union[str, datetime]):
        if isinstance(submit_deadline, str):
            thesis.submit_deadline = parse_date(submit_deadline)
        if isinstance(submit_deadline, datetime):
            thesis.submit_deadline = submit_deadline.date()
        return thesis.submit_deadline

    def _load_reviewer(self, reviewer: str):
        from apps.accounts.models import User
        from django.contrib.auth.models import Group

        if ' ' not in reviewer:
            # probably username, internal
            user = User.school_users.teachers().filter(username=reviewer).first()
            if not user:
                raise ValidationError(_('Unknown user {}').format(reviewer))
            return user

        # external
        user = User.objects.get_or_create_from_name(name=reviewer, thesis_id=None)[0]
        user.groups.add(Group.objects.get_or_create(name='teacher')[0])
        user.is_active = False

        return user

    @property
    def columns_definition(self):
        from apps.thesis.models import Category

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
                _('Submit deadline, DD.MM.YYYY, not required'),
                'calendar',
                self._set_submit_deadline,
            ),
        ]
