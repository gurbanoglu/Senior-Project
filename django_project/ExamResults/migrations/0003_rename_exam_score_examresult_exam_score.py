# Generated by Django 4.0.5 on 2022-07-30 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ExamResults', '0002_alter_examresult_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examresult',
            old_name='exam_score',
            new_name='exam_Score',
        ),
    ]
