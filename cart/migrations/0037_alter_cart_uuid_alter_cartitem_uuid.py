# Generated by Django 4.2.5 on 2024-06-28 11:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0036_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('178c7fb1-9aa8-49a4-afbe-736e2bb13a63')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('0272e5ff-5708-48ed-bf42-74c69c477629')),
        ),
    ]
