from django.db import connection

def delete_quizsession_forcefully(session_id):
    with connection.cursor() as cursor:
        try:
            cursor.execute("DELETE FROM quizapp_quizsession WHERE id = %s", [session_id])
        except:
            print("Error - unable to delete quizsession")
