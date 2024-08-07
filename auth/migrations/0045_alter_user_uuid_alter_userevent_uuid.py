# Generated by Django 4.2.5 on 2024-07-03 05:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0044_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c1cdcd0a-7741-4de7-9262-e7d56d9ab4a0')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c1cdcd0a-7741-4de7-9262-e7d56d9ab4a0')),
        ),
    ]
