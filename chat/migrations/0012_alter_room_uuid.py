# Generated by Django 4.2.5 on 2024-06-02 14:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('077f01c0-d421-48e2-8621-f1ef568146ce')),
        ),
    ]
