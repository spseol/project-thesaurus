import django.contrib.postgres.fields
import django.contrib.postgres.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0008_auto_20231023_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='grades',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveSmallIntegerField(
                    choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E'), (6, 'F')],
                    help_text='As value between 1 and 6 inclusive.',
                    validators=[
                        django.core.validators.MinValueValidator(1),
                        django.core.validators.MaxValueValidator(6),
                    ],
                ),
                size=None,
                validators=[
                    django.contrib.postgres.validators.ArrayMinLengthValidator(5),
                    django.contrib.postgres.validators.ArrayMaxLengthValidator(6),
                ],
                verbose_name='Grades',
            ),
        ),
        migrations.AlterField(
            model_name='review',
            name='grade_proposal',
            field=models.PositiveSmallIntegerField(
                choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E'), (6, 'F')],
                help_text='As value between 1 and 6 inclusive.',
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(6),
                ],
                verbose_name='Proposed grade',
            ),
        ),
    ]
