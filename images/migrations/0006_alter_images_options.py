# Generated by Django 5.1.5 on 2025-02-07 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_images_image_type_images_size'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='images',
            options={'ordering': ['-is_profile_image']},
        ),
    ]
