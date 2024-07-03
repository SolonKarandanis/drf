# Generated by Django 4.2.5 on 2024-07-03 05:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0021_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('34b57e39-b23d-452a-9411-41290362c2be')),
        ),
    ]
