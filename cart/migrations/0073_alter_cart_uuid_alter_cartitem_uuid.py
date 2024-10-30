# Generated by Django 5.1.2 on 2024-10-30 13:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0072_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('82aee563-f35f-426b-9e01-8adf911405e4')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('6f7c4d18-cca1-4c9a-8598-76426ee36530')),
        ),
    ]