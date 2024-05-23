# Generated by Django 4.2.5 on 2023-12-04 07:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('976d5f27-d528-47fa-b91f-a003162746f7')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('f068903f-44ba-41ef-bf37-37ff28e6f55e')),
        ),
    ]