# Generated by Django 5.1.1 on 2024-10-15 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0003_userresponse_selected_answers_alter_quizsession_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponse',
            name='selected_answers',
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='selected_answer',
            field=models.CharField(blank=True, default=' ', max_length=200),
            preserve_default=False,
        ),
    ]