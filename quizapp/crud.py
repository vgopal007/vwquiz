from .models import QuizSession
from .models import UserResponse
import uuid
from datetime import datetime
from datetime import date

def create_quizsession(user,subject):
    quiz_session = QuizSession(user=user,quiz=subject)
    quiz_session.save()
    print ("quiz_session : ", quiz_session)
    return quiz_session
    
def create_userresponse(session,question):
    print ("Passed to UserResponse  : ", session, question)
   
    userresponse = UserResponse(session=session, question=question)
    print ("UserResponse  : ", userresponse)
    userresponse.save()

    return userresponse
    