# Generated by Django 4.2.5 on 2024-07-02 05:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0018_alter_room_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('849ec70d-9242-4ccf-b8a3-3ed68caa9516')),
        ),
    ]
