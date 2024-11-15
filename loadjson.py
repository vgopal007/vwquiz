# Ths program reads JSON file and inserts data into the vwquiz database
# It calls db_operations.db for database operations
import json
import uuid
from datetime import date
from vwquizfunclib import select_category, generate_uuid
from db_operations import connect_db, close_db, fetch_categories, fetch_subject_id, insert_question, insert_topic

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON format in {file_path}.")
        return None
    return None

def check_question_exists(cursor, question_text):
    """Check if question text already exists."""
    cursor.execute("SELECT 1 FROM quizapp_question WHERE question = ?", (question_text,))
    return cursor.fetchone() is not None

def check_topic_exists(cursor, topic):
     cursor.execute("SELECT uid FROM quizapp_topics WHERE topic = ?", (topic,))
     result = cursor.fetchone()
     return result[0] if result else None  
    
def validate_question(question):
    
    required_fields = ['question', 'topic', 'type', 'choices', 'correct_answer']
    """ if question['type']<>"IN":
       required_fields.append('choices')        
    """
    if not all(field in question for field in required_fields):
        print("Missing required fields.")
        return False

    if question['type'] == "IN":
        if len(question['choices']) != 0:
            print("IN type question should have no option")
            return False
    elif question['type'] == "RB":
        if len(question['choices']) < 2:
            print("RB type question should have at least 2 options.")
            return False
    elif question['type'] == "CB":
        if len(question['choices']) < 2:
            print("CB type question should have more than 2 options.")
            return False

    return True


    
def main():
    dryrun = input("Dry run? Yes for display only, No to import data into the database: Yes/No: ")
    filename = input("Enter the filename of the JSON File: ")
    source = input("Enter the source name(ChatGPT/Meta/Copilot..) : ")
 
    conn, cursor = connect_db()
    categories = fetch_categories(cursor)
    cat = select_category(categories)
    subject_id = fetch_subject_id(cursor, cat)

    if subject_id:
        subject_id = str(subject_id).replace('-', '')
        data = read_json_file(filename)
        if data:
            for question in data:
                if not validate_question(question):
                    continue
                question_id = generate_uuid()
                qtext = question['question']
                qtopic = question['topic']

 
                answer = question['correct_answer']
                difficulty_level = question['difficulty_level']
                reference = question['reference']
                answer_explanation = question['answer_explanation']
                qtype = question['type']
                created_at = date.today()
                updated_at = date.today()
   
                topic_id=check_topic_exists(cursor, qtopic)
                if not topic_id:
                    print("Adding a new topic to {cat} : ", qtopic)
                    topic_id = generate_uuid()
                    topic_data = (
                        topic_id, created_at, updated_at, qtopic, subject_id, 0
                        )
                    if dryrun.lower().startswith("n"):
                        insert_topic(cursor, topic_data)
                    else:
                        print(topic_data)
 
   
                if check_question_exists(cursor, qtext):
                    print(f"Question '{qtext}' already exists. Skipping.")
                    continue

                if question['type']=="IN":
                    optionstext=str(answer)
                else:
                    optionstext=question['choices']            
  
                delete_flag=False
                qc_passed=False

                question_data = (
                    question_id, created_at, updated_at, qtype, qtext, topic_id, 1,
                    answer_explanation, difficulty_level, reference, source, subject_id, delete_flag, qc_passed
                )

                if dryrun.lower().startswith("n"):
                    insert_question(cursor, question_data)
                else:
                    print(question_data)
                    
          
                #optionstrue = [x==answer for x in options]
                optionstrue = [x in answer for x in optionstext]
                lookup_dict = dict(zip(optionstext, optionstrue))

                if question['type']=="IN":
                    answer=str(question['correct_answer'])
                    answer_id = generate_uuid()
                    is_correct=True
                    if dryrun.lower().startswith("n"):
                        cursor.execute('INSERT INTO quizapp_answer (uid, created_at, updated_at,answer,is_correct,question_id) VALUES (?, ?, ?, ?, ?, ?)', (answer_id, created_at, updated_at,answer,is_correct,question_id))
                        conn.commit()
                    else:
                        print (answer_id, created_at, updated_at,answer,is_correct,question_id)
          
                else:    
                # Iterate through List OptionsText and get corresponding values from List OptionsTrue
                    for a_option in optionstext:
                        answer_id = generate_uuid()
 
                        is_correct = lookup_dict.get(a_option) 
                
                        if dryrun.lower().startswith("n"): 
                            cursor.execute('INSERT INTO quizapp_answer (uid, created_at, updated_at,answer,is_correct,question_id) VALUES (?, ?, ?, ?, ?, ?)', (answer_id, created_at, updated_at,a_option,is_correct,question_id))
                            conn.commit()
                        else:
                            print (answer_id, created_at, updated_at,a_option,is_correct,question_id)
                              

    close_db(conn)

if __name__ == "__main__":
    main()
    
