# Generated by Django 4.2.5 on 2024-07-03 05:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0045_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('928be6a9-4ca9-47d4-8b5f-8c7f8506c50b')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('928be6a9-4ca9-47d4-8b5f-8c7f8506c50b')),
        ),
    ]