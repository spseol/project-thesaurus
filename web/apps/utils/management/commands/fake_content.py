import string
from datetime import date
from random import choice, randint, sample

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django_seed import Seed

from apps.thesis.models import Thesis, Reservation, Category


class Command(BaseCommand):
    help = "Generates fake content."

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for title in 'SE SL VE VT'.split(' '):
            Category.objects.update_or_create(title=title)

        categories = tuple(Category.objects.all())
        seeder = Seed.seeder(locale='cz_CZ')
        seeder.add_entity(get_user_model(), 30)
        seeder.add_entity(Thesis, 200, dict(
            registration_number=lambda *_: ''.join((choice(string.ascii_uppercase), str(randint(100, 999)))),
            published_at=lambda *_: date(randint(2004, 2020), choice((4, 5)), 1),
            category=lambda *_: choice(categories)
        ))
        seeder.add_entity(Reservation, 10)

        teacher = Group.objects.get_or_create(name='teacher')[0]
        for user in sample(list(get_user_model().objects.all()), 10):
            teacher.user_set.add(user)

        with transaction.atomic():
            seeder.execute()
