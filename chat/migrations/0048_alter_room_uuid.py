# Generated by Django 5.1.2 on 2024-10-22 05:20

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0047_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dffeeafb-bb31-496d-a030-b86e01829160')),
        ),
    ]
