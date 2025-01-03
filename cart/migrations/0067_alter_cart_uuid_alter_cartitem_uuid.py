# Generated by Django 5.1.2 on 2024-10-22 05:17

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0066_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c70dfac7-0e61-4aa5-aad0-0fa23cd7a1f2')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('8ecbcd2d-b33d-4a32-92e8-75f28ec189ae')),
        ),
    ]
