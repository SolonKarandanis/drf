# Generated by Django 4.2.5 on 2023-11-30 12:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_rename_user_id_cart_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('eae120af-df97-4a93-a5f0-9d024a033787')),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('46102e4d-3c87-4f41-823c-72f1bcedb6e3')),
        ),
    ]
