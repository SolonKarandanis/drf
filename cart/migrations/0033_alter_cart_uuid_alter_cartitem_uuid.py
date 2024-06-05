# Generated by Django 4.2.5 on 2024-06-05 12:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0032_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('67af1e2d-eb7f-4f7f-8ab7-8b589814dd2f')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('41768a2f-d214-457b-b775-23e3a7cdf3a4')),
        ),
    ]
