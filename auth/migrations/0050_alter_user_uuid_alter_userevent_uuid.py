# Generated by Django 4.2.5 on 2024-09-02 16:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0049_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('0a149d55-3a4b-43b6-841c-361e5c742dbf')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('0a149d55-3a4b-43b6-841c-361e5c742dbf')),
        ),
    ]