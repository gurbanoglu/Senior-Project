# Generated by Django 4.1 on 2025-05-15 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_profile_m_facial_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='m_Profile_Image_URL',
        ),
        migrations.AlterField(
            model_name='profile',
            name='m_Profile_Image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/', verbose_name='Profile Image'),
        ),
    ]
