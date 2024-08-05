# Generated by Django 5.0.6 on 2024-06-26 22:04

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dicom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_id', models.CharField(max_length=255)),
                ('patient_name', models.CharField(max_length=255)),
                ('study_date', models.DateField()),
                ('study_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='dicomimage',
            old_name='modalities_in_study',
            new_name='modality',
        ),
        migrations.RemoveField(
            model_name='dicomimage',
            name='accession_number',
        ),
        migrations.RemoveField(
            model_name='dicomimage',
            name='number_of_series',
        ),
        migrations.RemoveField(
            model_name='dicomimage',
            name='study_date',
        ),
        migrations.RemoveField(
            model_name='dicomimage',
            name='study_description',
        ),
        migrations.AddField(
            model_name='dicomimage',
            name='body_part',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='dicomimage',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dicomimage',
            name='study',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='dicom.study'),
            preserve_default=False,
        ),
    ]