# Generated by Django 5.1.2 on 2024-10-10 04:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0049_alter_order_is_shipped_alter_order_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('9668d44d-8624-4d18-8f79-1c0d038c582c')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('267f7637-3dcd-4f42-ab93-4c50fe2d8162')),
        ),
    ]
