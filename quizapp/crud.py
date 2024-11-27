from .models import QuizSession
from .models import UserResponse
import uuid
from datetime import datetime
from datetime import date

def create_quizsession(session_data):
    quiz_session = QuizSession(
        user_id=session_data['user_obj'], 
        subject=session_data['types_obj'], 
        total_questions=session_data['test_numberofquestions'], 
        test_duration_minutes=session_data['test_duration_minutes'],
        test_mode=session_data['test_mode']
    )
    if session_data['test_mode']=='T':
        quiz_session.save()
    print("quiz_session :", quiz_session)
    return quiz_session

def create_userresponse(session,question):
    
    userresponse = UserResponse(session=session, question=question)
    userresponse.save()

    return userresponse
    
    