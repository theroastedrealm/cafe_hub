# Generated by Django 5.0.6 on 2024-08-22 02:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafePosts', '0002_rename_user_post_author_and_more'),
        ('main', '0006_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.branch'),
        ),
        migrations.AddField(
            model_name='post',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.branch'),
        ),
    ]
