# Generated by Django 4.2.5 on 2023-11-30 12:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('581db888-e534-4757-b909-021909271ac4')),
        ),
    ]
