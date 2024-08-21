# Generated by Django 5.0.6 on 2024-08-13 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='products/')),
                ('amazon_link', models.URLField(max_length=500)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
