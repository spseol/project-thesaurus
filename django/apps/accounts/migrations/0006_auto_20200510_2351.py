# Generated by Django 3.0.6 on 2020-05-10 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200510_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='degree_after',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Degree after'),
        ),
        migrations.AlterField(
            model_name='user',
            name='degree_before',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Degree before'),
        ),
    ]
