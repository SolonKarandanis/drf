# Generated by Django 4.2.5 on 2024-09-23 08:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0051_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('de0da1e6-0cc7-4b2f-8ce5-950fc64d8db4')),
        ),
    ]