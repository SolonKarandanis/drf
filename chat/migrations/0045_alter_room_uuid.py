# Generated by Django 5.1.2 on 2024-10-22 04:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0044_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('0ba94abe-9229-4216-b9c3-d0caf8eea797')),
        ),
    ]