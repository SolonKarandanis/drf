# Generated by Django 5.1.2 on 2024-10-22 05:17

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0061_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('e164d7ee-6678-43f1-9d33-00870b8a11eb')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('6ce1b4cd-f7a1-4a23-9581-ebc9046577df')),
        ),
    ]