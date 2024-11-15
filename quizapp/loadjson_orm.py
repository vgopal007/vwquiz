# loadjson_orm.py
from .models import Question, Answer
import json
from datetime import date
from uuid import uuid4

def load_json_data(data):
    for question in data:
        question_id = uuid4()
        qtext = question['question']
        qtopic = question['topic']
        qtopic = question['topic']
        try:
            topic_obj = Topics.objects.get(topic=qtopic)
        except Topics.DoesNotExist:
            # Create a new topic
            topic_obj = Topics(topic=qtopic)
            topic_obj.save()           
            print(f"New topic '{qtopic}' created.")
            
        answer = question['correct_answer']
        difficulty_level = question['difficulty_level']
        reference = question['reference']
        answer_explanation = question['answer_explanation']
        qtype = question['type']
        created_at = date.today()
        updated_at = date.today()
 
        question_obj = Question(
            uid=question_id,
            created_at=created_at,
            updated_at=updated_at,
            type=qtype,
            text=qtext,
            topic=qtopic,
            difficulty_level=difficulty_level,
            reference=reference,
            answer_explanation=answer_explanation
        )
        question_obj.save()

        for option in question['options']:
            answer_id = uuid4()
            answer_obj = Answer(
                uid=answer_id,
                created_at=created_at,
                updated_at=updated_at,
                answer=option,
                is_correct=(option == answer),
                question=question_obj
            )
            answer_obj.save()
			