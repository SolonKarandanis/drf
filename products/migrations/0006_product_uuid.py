# Generated by Django 4.2.5 on 2023-11-30 12:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('d3c4b6f7-23ba-4944-8c4b-d8d190742134')),
        ),
    ]
