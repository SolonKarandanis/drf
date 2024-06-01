# Generated by Django 4.2.5 on 2024-06-01 07:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0030_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('a5491a64-0ce3-4988-b483-52441b2c54ca')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('042d781f-ec3b-4a33-a984-65cb1b83ea6f')),
        ),
    ]
