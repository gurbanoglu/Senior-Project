# Generated by Django 4.1 on 2025-05-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profile_m_facial_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='m_Facial_Image_URL',
            field=models.URLField(default='https://res.cloudinary.com/dybmcxawv/image/upload/v1747032528/facial_images/default_facial_image.jpg', max_length=500),
        ),
    ]
