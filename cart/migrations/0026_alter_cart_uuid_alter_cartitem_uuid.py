# Generated by Django 4.2.5 on 2024-05-24 12:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0025_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('af213fe6-57f8-4ab0-b91f-ba3962f4807c')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('a819c2f9-4aed-434a-bcb6-4029f09237da')),
        ),
    ]
