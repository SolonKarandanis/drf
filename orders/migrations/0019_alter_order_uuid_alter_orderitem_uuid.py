# Generated by Django 4.2.5 on 2024-05-23 13:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ed1735c0-59b3-4fee-bc88-95dccef95e5f')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('285ca503-10b5-46d8-9abf-d29128b67738')),
        ),
    ]
