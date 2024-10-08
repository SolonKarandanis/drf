# Generated by Django 5.1.2 on 2024-10-10 03:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0048_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_shipped',
            field=models.BooleanField(db_default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ca8b5d9e-ee53-46ba-bdc9-c7099f2659b8')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('0e932876-6281-4a75-a97a-a238458e3353')),
        ),
    ]
