# Generated by Django 4.2.5 on 2024-07-02 05:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0041_userdetails_country_alter_user_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('de245f79-1dbe-4d17-bd76-e742cbc4c38b')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('de245f79-1dbe-4d17-bd76-e742cbc4c38b')),
        ),
    ]
