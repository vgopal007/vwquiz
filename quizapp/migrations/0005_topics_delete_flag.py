# Generated by Django 4.2.16 on 2024-11-14 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0004_rename_qc_paased_question_qc_passed'),
    ]

    operations = [
        migrations.AddField(
            model_name='topics',
            name='delete_flag',
            field=models.BooleanField(default=False),
        ),
    ]
