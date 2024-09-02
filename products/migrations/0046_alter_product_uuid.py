# Generated by Django 4.2.5 on 2024-09-02 16:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0045_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('5ced48da-2191-48d2-8b12-e2e062f00c60')),
        ),
    ]
