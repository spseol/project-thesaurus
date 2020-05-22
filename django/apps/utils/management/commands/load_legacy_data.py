import sqlite3
from typing import Optional

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_date
from django.utils.text import slugify

from apps.accounts.models import User
from apps.thesis.models import Thesis, Category


class Command(BaseCommand):
    help = "Loads legacy data."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._conn = None

        self._student_group = Group.objects.get_or_create(name='student')[0]
        self._teacher_group = Group.objects.get_or_create(name='teacher')[0]

    def add_arguments(self, parser):
        parser.add_argument('file')

    @transaction.atomic
    def handle(self, *args, **options):
        self._conn = sqlite3.connect(options.get('file'))
        self._conn.row_factory = sqlite3.Row
        r = self._conn.execute("""
        SELECT k.*,
            o.jmeno as o_jmeno,
            v.jmeno as v_jmeno
        FROM knihy k
            inner join oponenti o ON k.oponent = o.id
            inner join oponenti v ON k.vedouci = v.id
            order by k.ID;
        """)

        # ['ID', 'ev_cislo', 'prace', 'ajmeno', 'vedouci', 'oponent', 'edatum', 'rok', 'typ', 'datumpridani', 'trida', 'souhlas', 'stav', 'abstrakt']
        # [152, 'S156', 'Syndrom CAN', 'And Klára ', 30,      1,     '2015-04-13', '2012-04-01', 'SL', '2015-04-13',
        # 'L4', 1, 'Dostupná', None]

        for row in r.fetchall():  # type:  sqlite3.Row
            if Thesis.objects.filter(registration_number=row['ev_cislo']).exists():
                continue

            print(tuple(row))
            t = Thesis(
                registration_number=row['ev_cislo'],
                title=row['prace'],
                category=Category.objects.get_or_create(title=row['typ'])[0],
                published_at=parse_date(row['rok']),
                reservable=str(row['souhlas']) == '1',
                state=Thesis.State.PUBLISHED,
            )

            t.supervisor = self.get_or_create_user(name=row['v_jmeno'], thesis_id=None)
            t.opponent = self.get_or_create_user(name=row['o_jmeno'], thesis_id=None)

            t.opponent and self._teacher_group.user_set.add(t.opponent)
            t.supervisor and self._teacher_group.user_set.add(t.supervisor)

            for name in row['ajmeno'].split(','):
                author = self.get_or_create_user(name=name, thesis_id=row['ID'])
                author.school_class = row['trida']
                self._student_group.user_set.add(author)
                t.authors.add(author)
                author.save(update_fields=['school_class'])

            t.save()
        self._teacher_group.save()
        self._student_group.save()

        self._fix_wrong_users()

    @staticmethod
    def get_or_create_user(*, name: str, thesis_id: Optional[str]) -> Optional[User]:

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

        user, was_created = User.objects.get_or_create(
            username=username,
            defaults=dict(
                last_name=last_name.strip(),
                first_name=first_name.strip(),
                degree_after=degree_after or None,
                degree_before=''.join(degrees_before[1:]).replace(' ', '').replace('.', '. ') or None,
                is_active=False,  # activation by ldap sync
            ),
        )

        if was_created:
            print(f"User {name} has been created.")

        return user

    def _fix_wrong_users(self):
        for user in User.objects.filter(first_name__iregex=r'(Ing|Mgr)\.'):
            try:
                correct = User.objects.exclude(id=user.id).exclude(
                    first_name__contains='.',
                ).get(
                    groups=self._teacher_group,
                    last_name=user.last_name,
                )
            except User.MultipleObjectsReturned:
                print('Cannot fix, multiple targets', user)
                continue
            except User.DoesNotExist:
                print('Cannot fix, not found correct', user)
                continue

            Thesis.objects.filter(opponent=user).update(opponent=correct)
            Thesis.objects.filter(supervisor=user).update(supervisor=correct)

            user.groups.set([])
            user.delete()
