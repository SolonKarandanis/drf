# Generated by Django 4.2.5 on 2024-09-21 06:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0027_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('8b877d33-86e2-4285-ac90-dea33c7ae45a')),
        ),
    ]