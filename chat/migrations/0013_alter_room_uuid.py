# Generated by Django 4.2.5 on 2024-06-05 12:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('a096ae3e-77da-4aa4-a73c-5d04a1a18376')),
        ),
    ]
