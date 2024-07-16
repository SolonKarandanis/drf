# Generated by Django 4.2.5 on 2024-07-03 05:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0043_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('cab28672-3159-42a7-9d90-d4b7cff60bef')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('cb86a7a2-610c-4872-b3e6-f5b8819995e8')),
        ),
    ]