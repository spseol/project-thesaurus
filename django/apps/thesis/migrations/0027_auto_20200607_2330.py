# Generated by Django 3.0.7 on 2020-06-07 21:30

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thesis', '0026_thesis_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='note',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='Additional note'),
        ),
    ]
