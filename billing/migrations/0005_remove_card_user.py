# Generated by Django 4.2.5 on 2024-09-21 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_card_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='user',
        ),
    ]