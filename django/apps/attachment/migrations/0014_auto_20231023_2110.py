# Generated by Django 3.2.14 on 2023-10-23 19:10

import apps.attachment.models.attachment
from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attachment', '0013_remove_typeattachment_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='content_type',
            field=models.CharField(choices=[('application/pdf', 'pdf'), ('image/png', 'png'), ('application/zip', 'zip'), ('application/x-rar-compressed', 'rar'), ('application/x-tar', 'tar'), ('application/gzip', 'gz'), ('application/x-zip-compressed', 'zip')], max_length=64),
        ),
        migrations.AlterField(
            model_name='typeattachment',
            name='allowed_content_types',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(choices=[('application/pdf', 'pdf'), ('image/png', 'png'), ('application/zip', 'zip'), ('application/x-rar-compressed', 'rar'), ('application/x-tar', 'tar'), ('application/gzip', 'gz'), ('application/x-zip-compressed', 'zip')], max_length=64), blank=True, default=apps.attachment.models.attachment._default_allowed_content_types, help_text='Dostupné možnosti: application/pdf, image/png, application/zip, application/x-rar-compressed, application/x-tar, application/gzip, application/x-zip-compressed', size=None, verbose_name='List of allowed mime/content types'),
        ),
    ]