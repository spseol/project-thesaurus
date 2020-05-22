from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.db import transaction

DATA = """
manager	Can view User
manager	Can add Attachment
manager	Can change Attachment
manager	Can delete Attachment
manager	Can view Attachment
manager	Can change Reservation
manager	Can delete Reservation
manager	Can view Reservation
manager	Can add Thesis
manager	Can change Thesis
manager	Can delete Thesis
manager	Can view Thesis
manager	Can add Thesis author relation
manager	Can change Thesis author relation
manager	Can delete Thesis author relation
manager	Can view Thesis author relation
manager	Can add Review
manager	Can change Review
manager	Can delete Review
manager	Can view Review
manager	Can view Category
student	Can view Thesis
student	Can view Category
student	Can add Reservation
student	Can view Reservation
teacher	Can view Thesis
teacher	Can add Review
teacher	Can view Review
teacher	Can view User
teacher	Can view Attachment
teacher	Can view Category
""".strip().split('\n')


class Command(BaseCommand):
    help = "Loads initial perms setup for groups student/teacher/manager."

    @transaction.atomic()
    def handle(self, *args, **kwargs):
        for line in DATA:
            g_name, p_name = line.split('\t')

            g: Group = Group.objects.get_or_create(name=g_name)[0]
            g.permissions.add(
                Permission.objects.get(name=p_name)
            )
