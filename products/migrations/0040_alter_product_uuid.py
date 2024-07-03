# Generated by Django 4.2.5 on 2024-07-03 05:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0039_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('5310d821-d45d-4d03-ba6c-b83bcaf611c2')),
        ),
    ]
