# Generated by Django 5.0.3 on 2024-03-19 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_customuser_exp_customuser_specialisation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
