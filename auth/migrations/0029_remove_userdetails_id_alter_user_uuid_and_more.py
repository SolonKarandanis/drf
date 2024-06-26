# Generated by Django 4.2.5 on 2024-05-24 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0028_alter_user_uuid_userdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='id',
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('93f4b84d-fd2c-4396-b0c7-6ae973f99c65')),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
