# Generated by Django 5.0.6 on 2024-06-25 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0003_contactus_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='institution',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
