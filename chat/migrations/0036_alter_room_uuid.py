# Generated by Django 5.1.2 on 2024-10-10 05:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0035_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('bc610fed-d1da-424e-948e-ad759705c735')),
        ),
    ]