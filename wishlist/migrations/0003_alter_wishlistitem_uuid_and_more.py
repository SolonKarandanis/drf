# Generated by Django 5.1.5 on 2025-04-10 05:16

import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0082_alter_product_uuid'),
        ('wishlist', '0002_wishlistitem_attributes_alter_wishlistitem_uuid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('14588fc3-dd56-4dce-b335-aaab790cecb7')),
        ),
        migrations.AddIndex(
            model_name='wishlistitem',
            index=models.Index(fields=['user_id'], name='wishlist_item_user_id'),
        ),
    ]
