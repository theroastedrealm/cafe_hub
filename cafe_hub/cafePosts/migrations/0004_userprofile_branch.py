# Generated by Django 5.0.6 on 2024-08-22 04:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafePosts', '0003_comment_branch_post_branch'),
        ('main', '0006_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.branch'),
        ),
    ]
