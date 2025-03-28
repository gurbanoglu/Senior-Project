# Generated by Django 4.0.5 on 2022-08-31 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_insession_roommember_m_insession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roommember',
            name='m_insession',
            field=models.BooleanField(default=True, verbose_name='In Session'),
        ),
        migrations.AlterField(
            model_name='roommember',
            name='m_name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='roommember',
            name='m_roomName',
            field=models.CharField(max_length=200, verbose_name='Room Name'),
        ),
        migrations.AlterField(
            model_name='roommember',
            name='m_userID',
            field=models.CharField(max_length=1000, verbose_name='User ID'),
        ),
    ]
