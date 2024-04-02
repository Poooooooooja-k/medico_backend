# Generated by Django 5.0.3 on 2024-04-02 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_blogpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarousalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='carousal/')),
            ],
        ),
    ]