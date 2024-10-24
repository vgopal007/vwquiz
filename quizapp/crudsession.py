from .models import quizsession
import uuid
from datetime import datetime
from datetime import date

def create_quizsession(user):
    created_at = date.today()
    updated_at = date.today()
    session_id = uuid.uuid4()
    session_id = str(session_id).replace('-', '')
    quiz = subject 
    score = 0  
    quizsession = quizsession(user=user, score=score,quiz=subject)
    quizsession.save()
    return quizsession
    
