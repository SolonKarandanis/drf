# Generated by Django 4.2.5 on 2024-05-24 12:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('8653b7fb-0536-4179-a61d-5e242342ddcb')),
        ),
    ]
