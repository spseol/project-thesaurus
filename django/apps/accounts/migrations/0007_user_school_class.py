# Generated by Django 3.0.6 on 2020-05-22 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200510_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='school_class',
            field=models.CharField(blank=True, default='', max_length=8, null=True, verbose_name='School class'),
        ),
    ]
