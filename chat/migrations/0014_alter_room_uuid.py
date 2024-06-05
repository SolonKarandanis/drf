# Generated by Django 4.2.5 on 2024-06-05 13:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('f9d2fcdf-4a66-4095-99b6-ae4f4276e661')),
        ),
    ]
