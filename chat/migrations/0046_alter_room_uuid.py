# Generated by Django 5.1.2 on 2024-10-22 04:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0045_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dccd1c0b-3420-4892-be39-b0fa39607cba')),
        ),
    ]