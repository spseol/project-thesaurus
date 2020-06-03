import sqlite3

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_date

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
                note=dict(imported_from=tuple(row))
            )

            t.supervisor = User.objects.get_or_create_from_name(name=row['v_jmeno'], thesis_id=None)[0]
            t.opponent = User.objects.get_or_create_from_name(name=row['o_jmeno'], thesis_id=None)[0]

            t.opponent and self._teacher_group.user_set.add(t.opponent)
            t.supervisor and self._teacher_group.user_set.add(t.supervisor)

            for name in row['ajmeno'].split(','):
                author = User.objects.get_or_create_from_name(name=name, thesis_id=row['ID'])[0]
                author.school_class = row['trida']
                self._student_group.user_set.add(author)
                t.authors.add(author)
                author.save(update_fields=['school_class'])

            t.save()
        self._teacher_group.save()
        self._student_group.save()

        self._fix_wrong_users()



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
