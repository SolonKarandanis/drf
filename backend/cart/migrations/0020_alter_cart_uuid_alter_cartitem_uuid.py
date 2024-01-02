# Generated by Django 4.2.5 on 2024-01-02 08:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0019_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('40dfc21e-42f0-4712-aa41-2bd41d571305')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('dce49c1c-fe21-44cd-b402-4ae8688d0a57')),
        ),
    ]
