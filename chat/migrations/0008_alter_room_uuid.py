# Generated by Django 4.2.5 on 2024-05-24 12:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ef9575b3-0b4f-4511-876f-9d3e81e3bb6b')),
        ),
    ]