# Generated by Django 4.2.5 on 2023-10-24 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inventory',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
