# Generated by Django 4.2.5 on 2024-06-02 14:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0030_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('97579769-f523-44a0-999e-bbac4b143f1c')),
        ),
    ]
