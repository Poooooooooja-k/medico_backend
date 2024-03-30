# Generated by Django 5.0.2 on 2024-03-29 12:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_alter_customuser_specialisation_alter_document_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
