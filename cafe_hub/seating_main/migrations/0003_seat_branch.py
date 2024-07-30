# Generated by Django 5.0.7 on 2024-07-30 19:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_customuser_branch'),
        ('seating_main', '0002_seat_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.branch'),
        ),
    ]
