from django.db import migrations, models


def set_ap_grade_type(apps, schema_editor):
    Category = apps.get_model('thesis', 'Category')
    Category.objects.filter(title__in=['Vt', 'Ve', 'Dt', 'De']).update(grade_type='ap')


class Migration(migrations.Migration):

    dependencies = [
        ('thesis', '0030_alter_thesis_registration_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='grade_type',
            field=models.CharField(
                choices=[('dmp', 'DMP (SPŠ)'), ('ap', 'AP (VOŠ)')],
                default='dmp',
                max_length=3,
                verbose_name='Grade type',
            ),
        ),
        migrations.RunPython(set_ap_grade_type, migrations.RunPython.noop),
    ]
