# Generated by Django 5.0.2 on 2024-04-10 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0014_remove_timeslot_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.FileField(blank=True, upload_to='profilepic/'),
        ),
    ]
