# Generated by Django 3.2.14 on 2023-10-23 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thesis', '0027_auto_20200607_2330'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thesis',
            options={'ordering': ['registration_number'], 'permissions': (('can_view_unpublished_theses', 'Can view unpublished theses'),), 'verbose_name': 'Thesis', 'verbose_name_plural': 'Theses'},
        ),
    ]