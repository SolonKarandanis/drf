# Generated by Django 5.1.2 on 2024-12-18 06:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0054_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('b64ead35-5c4c-4d3d-9f1b-410181edade5')),
        ),
    ]
