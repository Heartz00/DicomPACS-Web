# Generated by Django 4.2 on 2024-08-27 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=64, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('study_description', models.CharField(blank=True, max_length=255, null=True)),
                ('study_date', models.DateField()),
                ('modalities_in_study', models.CharField(max_length=255)),
                ('accession_number', models.CharField(max_length=64)),
                ('number_of_series', models.IntegerField()),
            ],
        ),
    ]
