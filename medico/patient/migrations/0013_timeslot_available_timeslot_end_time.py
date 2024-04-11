# Generated by Django 5.0.2 on 2024-04-09 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0012_customuser_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
