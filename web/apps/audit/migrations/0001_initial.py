from __future__ import unicode_literals

import os

from django.db import migrations

FILE = os.path.join(os.path.dirname(__file__), __file__.replace('.py', '.sql'))

with open(FILE) as f:
    SQL = f.read()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(SQL),
    ]
