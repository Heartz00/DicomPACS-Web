# Generated by Django 5.0.6 on 2024-06-30 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dicom', '0006_institution_study_upload_time_study_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicomimage',
            name='dicom_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]