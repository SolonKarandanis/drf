# Generated by Django 5.1.5 on 2025-03-24 06:55

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0059_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('adf72794-a141-469f-9aef-8f64759cd1c9')),
        ),
    ]
