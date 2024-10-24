# Generated by Django 5.1.2 on 2024-10-23 04:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0068_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ce880897-13c8-4596-a42b-3bab03f5fe6e')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('104b4529-af33-46e2-b37d-b819baabbd72')),
        ),
    ]