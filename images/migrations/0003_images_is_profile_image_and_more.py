# Generated by Django 4.2.5 on 2024-07-03 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_rename_user_images_uploaded_by_images_uploaded_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='is_profile_image',
            field=models.BooleanField(default=False),
        ),
        migrations.AddConstraint(
            model_name='images',
            constraint=models.UniqueConstraint(condition=models.Q(('is_profile_image', True)), fields=('object_id', 'is_profile_image'), name='one_user_profile_image'),
        ),
    ]
