# Generated by Django 5.0.3 on 2024-04-11 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0019_blogpost_blog_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='created_by',
            field=models.CharField(default='admin@medico', max_length=100),
        ),
    ]
