# Generated by Django 3.2.16 on 2025-01-08 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birthday', '0002_auto_20250108_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='birthday',
            name='image',
        ),
    ]
