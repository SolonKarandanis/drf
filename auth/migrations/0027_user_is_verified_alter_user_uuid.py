# Generated by Django 4.2.5 on 2024-05-23 13:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0026_user_bio_alter_user_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('42a0786b-4ced-4449-876c-bea053b70ebf')),
        ),
    ]
