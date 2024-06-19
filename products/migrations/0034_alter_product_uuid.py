# Generated by Django 4.2.5 on 2024-06-05 13:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('2daa6a3f-3e38-48fd-a5ca-b17900453804')),
        ),
    ]