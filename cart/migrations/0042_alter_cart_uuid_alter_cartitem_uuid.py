# Generated by Django 4.2.5 on 2024-07-03 05:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0041_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('e906fb85-dc17-46b9-b24d-f8dab49891a8')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('0b5560de-7a79-44c3-8203-22a0a2ba9660')),
        ),
    ]
