# Generated by Django 4.2.5 on 2024-07-03 05:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0023_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('f16518bd-7a9c-4deb-b736-35dd3b1b212b')),
        ),
    ]
