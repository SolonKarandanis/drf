# Generated by Django 5.1.2 on 2024-12-18 06:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0077_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('5c905438-e78d-454f-b336-6f23e8c4c954')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('5c905438-e78d-454f-b336-6f23e8c4c954')),
        ),
    ]
