# Generated by Django 4.2.5 on 2023-11-11 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cart_user_id'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='cart',
            new_name='cart_user_id',
            old_name='user_id',
        ),
    ]
