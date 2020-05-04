# Generated by Django 3.0.5 on 2020-05-04 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thesis', '0011_auto_20200429_2213'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='grade_proposal',
            field=models.CharField(default=None, max_length=8, verbose_name='Proposed grade'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='thesis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='review_thesis', to='thesis.Thesis'),
        ),
    ]