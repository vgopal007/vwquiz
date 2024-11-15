# Generated by Django 4.2.16 on 2024-11-12 22:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('question_type', models.CharField(choices=[('RB', 'Radio Button'), ('CB', 'Checkbox'), ('IN', 'Input')], default='RB', max_length=10)),
                ('question', models.CharField(max_length=100)),
                ('marks', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('answer_explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('difficulty_level', models.CharField(blank=True, max_length=20, null=True)),
                ('reference', models.CharField(max_length=100)),
                ('source', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuizSession',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('test_mode', models.CharField(choices=[('T', 'TEST'), ('P', 'PRACTICE')], default='P', max_length=1)),
                ('total_questions', models.IntegerField(blank=True, null=True)),
                ('correct_answers', models.IntegerField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('completed', models.BooleanField(default=False)),
                ('timed_out', models.BooleanField(default=False)),
                ('test_duration_minutes', models.IntegerField(default=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('subject_name', models.CharField(max_length=100)),
                ('domain', models.CharField(max_length=100)),
                ('test_duration_minutes', models.IntegerField(default=30)),
                ('test_numberofquestions', models.IntegerField(default=30)),
            ],
            options={
                'verbose_name_plural': 'Types',
            },
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('selected_answers', models.JSONField(blank=True, default=list)),
                ('selected_answer', models.CharField(blank=True, max_length=200)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_responses', to='quizapp.question')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_responses', to='quizapp.quizsession')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('topic', models.CharField(max_length=100, unique=True)),
                ('weight_perc', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types_topic', to='quizapp.types')),
            ],
            options={
                'verbose_name_plural': 'Topics',
            },
        ),
        migrations.AddField(
            model_name='quizsession',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types_session', to='quizapp.types'),
        ),
        migrations.AddField(
            model_name='quizsession',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types_question', to='quizapp.types'),
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics_question', to='quizapp.topics'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('answer', models.CharField(max_length=100)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answer', to='quizapp.question')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
