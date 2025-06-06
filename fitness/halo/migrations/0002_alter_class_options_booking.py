# Generated by Django 5.2.2 on 2025-06-04 22:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'ordering': ['datetime'], 'verbose_name_plural': 'Classes'},
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=100)),
                ('client_email', models.EmailField(max_length=200)),
                ('booked_at', models.DateTimeField(auto_now_add=True)),
                ('class_booked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='halo.class')),
            ],
        ),
    ]
