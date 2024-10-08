# Generated by Django 4.2.5 on 2024-09-02 16:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0046_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('8064e406-cd6e-4194-bce3-ac7d48a670a1')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('f6132422-1b99-4082-8c1b-e3ed38e726f0')),
        ),
    ]
