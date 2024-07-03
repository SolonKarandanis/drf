# Generated by Django 4.2.5 on 2024-07-03 05:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0041_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('a61b7a02-0e22-4eab-b533-ee622a29c55b')),
        ),
    ]
