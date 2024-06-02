# Generated by Django 4.2.5 on 2024-06-02 14:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0034_user_cv_user_uploaded_at_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('e8b84ac0-a959-4559-8030-4caf57d44186')),
        ),
    ]
