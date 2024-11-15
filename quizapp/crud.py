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
        test_duration_minutes=session_data['test_duration_minutes']
    )
    quiz_session.save()
    print("quiz_session :", quiz_session)
    return quiz_session

def create_userresponse(session,question):
    #print ("Passed to UserResponse  : ", session, question)
   
    userresponse = UserResponse(session=session, question=question)
    #print ("UserResponse  : ", userresponse)
    userresponse.save()

    return userresponse
    
    