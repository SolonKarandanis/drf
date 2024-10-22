# Generated by Django 5.1.2 on 2024-10-21 05:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0065_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('d16932bf-38fc-4e17-a5bc-809df1f58d52')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('d16932bf-38fc-4e17-a5bc-809df1f58d52')),
        ),
    ]