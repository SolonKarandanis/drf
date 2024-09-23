# Generated by Django 4.2.5 on 2024-09-23 08:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0052_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c6728016-f4c6-420f-ac6e-72b4e8ad3ee7')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('19680aa8-e4ef-49f2-acd9-bab902d5f548')),
        ),
    ]