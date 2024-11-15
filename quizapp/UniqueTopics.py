import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizapp.settings')

import django
django.setup()

from django.db.models import Count
from quizapp.models import Question, Topic, Types
# Get unique topics and question counts
topic_counts = Question.objects.values('subject__subject_name', 'topic').annotate(count=Count('id')).order_by('subject__subject_name', 'topic')

# Organize results
results = {}
for item in topic_counts:
    subject_name = item['subject__subject_name']
    topic_name = item['topic']
    count = item['count']
    
    if subject_name not in results:
        results[subject_name] = {}
    
    results[subject_name][topic_name] = count

# Print results
for subject, topics in results.items():
    print(f"Subject: {subject}")
    for topic, count in topics.items():
        print(f"  Topic: {topic}, Questions: {count}")