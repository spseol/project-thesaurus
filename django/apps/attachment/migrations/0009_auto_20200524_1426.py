# Generated by Django 3.0.6 on 2020-05-24 14:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('attachment', '0008_auto_20200518_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeattachment',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Order'),
        ),
    ]