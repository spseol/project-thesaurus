# Generated by Django 3.0.5 on 2020-04-24 19:00

from django.db import migrations
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('thesis', '0005_auto_20200424_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='order',
            field=positions.fields.PositionField(default=-1, verbose_name='Pořadí'),
        ),
    ]