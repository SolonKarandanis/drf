# Generated by Django 4.2.5 on 2024-05-24 12:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('1dd58665-a9ae-47e3-98d2-c6f550bc3d2d')),
        ),
    ]
