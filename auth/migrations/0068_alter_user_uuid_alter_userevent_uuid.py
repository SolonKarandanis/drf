# Generated by Django 5.1.2 on 2024-10-22 04:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0067_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('b2a5853a-03a2-48ae-a7c2-ce7731fe9d74')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('b2a5853a-03a2-48ae-a7c2-ce7731fe9d74')),
        ),
    ]
