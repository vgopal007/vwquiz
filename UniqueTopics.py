import sys
import os
import django
from django.db.models import Count
from quizapp.models import Question

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizapp.settings')
django.setup()

# Get unique topics and question counts
topic_counts = Question.objects.values('subject__subject_name', 'topic').annotate(count=Count('id')).order_by('subject__subject_name', 'topic')

# Organize and print results
results = {}
for item in topic_counts:
    subject_name = item['subject__subject_name']
    topic_name = item['topic']
    count = item['count']
    
    results.setdefault(subject_name, {})[topic_name] = count

for subject, topics in results.items():
    print(f"Subject: {subject}")
    for topic, count in topics.items():
        print(f"  Topic: {topic}, Questions: {count}")
        