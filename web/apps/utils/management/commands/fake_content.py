import string
from random import choice, randint

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django_seed import Seed

from apps.thesis.models import Thesis, Reservation, Category


class Command(BaseCommand):
    help = "Generates fake content."

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        seeder = Seed.seeder(locale='cz_CZ')

        seeder.add_entity(get_user_model(), 100)
        seeder.add_entity(Category, 10)
        seeder.add_entity(Thesis, 1000, dict(
            registration_number=lambda *_: ''.join((choice(string.ascii_uppercase), str(randint(100, 999))))
        ))
        seeder.add_entity(Reservation, 10)
        seeder.execute()
