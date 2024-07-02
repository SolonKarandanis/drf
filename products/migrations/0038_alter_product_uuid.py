# Generated by Django 4.2.5 on 2024-07-02 05:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('f7c58fa1-4aa0-4d38-b49f-82aa36b6ef81')),
        ),
    ]
