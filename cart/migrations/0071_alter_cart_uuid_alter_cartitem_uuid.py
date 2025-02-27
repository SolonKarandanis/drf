# Generated by Django 5.1.2 on 2024-10-24 06:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0070_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('0bf74814-8c13-4065-b45d-26b189efde0a')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('f846546f-0958-4fe5-b60e-fe343cff7758')),
        ),
    ]
