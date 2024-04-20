# Generated by Django 5.0.2 on 2024-04-19 06:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0026_slotbooking_payment_completed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('consultation_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.slotbooking')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_payments', to='patient.slotbooking')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='patient.slotbooking')),
            ],
        ),
    ]