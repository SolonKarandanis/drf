# Generated by Django 5.1.2 on 2024-10-25 07:58

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0074_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('6a1ec2e6-d739-4656-a07b-6ec09ef54073')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('6a1ec2e6-d739-4656-a07b-6ec09ef54073')),
        ),
    ]