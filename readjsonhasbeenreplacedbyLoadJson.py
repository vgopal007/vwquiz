# question_type can be RB for 1 answer, CB for checkox multiple answers, or IN for user input
import sqlite3
import json
import uuid
import random
import re
# import custom functions from vwquizfunclib.py
from  vwquizfunclib import select_category
from  vwquizfunclib import generate_uuid

def read_json_file(file_path):

    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON format in {file_path}.")
        return None



def main():
    dryrun= input("Dry run?  Yes for display only, No to import data into the database : Yes/No : ")
    source = input ("Enter the source name :")
    filename = input ("Enter the filename of the JSON File :")
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('vwquiz.db')
    cursor = conn.cursor()
    # Enable foreign key constraints, not ON by default!
    cursor.execute("PRAGMA foreign_keys = ON;")
    # Retrieve the list of categories from the quizapp_types table 
    cursor.execute('SELECT subject_name FROM quizapp_types')
    categories = [row[0] for row in cursor.fetchall()]

    cat = select_category(categories) # ask user to select a category
    # from django.db import models
    from datetime import datetime
    from datetime import date


    created_at = date.today()
    updated_at = date.today()

    cursor.execute("SELECT uid, subject_name FROM quizapp_types where subject_name=?", (cat,))

    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Category: {row[1]}")
        subject_id= row[0]

    subject_id = str(subject_id).replace('-', '')
    # UUID from Quizapp_Types of selected Category

    question=""
    cat=""
    options=[]
    optionstext=[]
    optionstrue=[]
    answer=""
    answerline=False
    answer_explanation=""
    q=0

    
    data = read_json_file(filename)

    if data:
        #questions = data['questions']
        for question in data: 
            question_id = generate_uuid()
            qtext=question['question']
            qtopic=question['topic']
            answer=question['correct_answer']
            difficulty_level=question['difficulty_level']
            reference=question['reference']
            answer_explanation=question['answer_explanation']
            qtype=question['type']
           
            if question['type']=="IN":
                optionstext=str(answer)
            else:
                optionstext=question['choices']            
                
 
            if dryrun=="No":    
                cursor.execute('INSERT INTO quizapp_question (uid, created_at, updated_at, question_type, question, topic, marks,answer_explanation,difficulty_level,reference,source, subject_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)',(question_id, created_at, updated_at,qtype, qtext,qtopic, 1,answer_explanation,difficulty_level,reference, source, subject_id) )
            else:    
                print(question_id, created_at, updated_at,qtype, qtext,qtopic, 1,answer_explanation,difficulty_level,reference, source, subject_id) 
            
  
          
            #optionstrue = [x==answer for x in options]
            optionstrue = [x in answer for x in optionstext]
            lookup_dict = dict(zip(optionstext, optionstrue))
            """
            if question['type']=="true_false":
                   print("OptionsText is ", optionstext)
                   print("OptionsTrue is ", optionstrue)
                   print("Answer is ", answer)
                   print("lookup_dict=", lookup_dict)
                   """
            if question['type']=="IN":
              answer=str(question['correct_answer'])
              answer_id = generate_uuid()
              is_correct=True
              if dryrun=="No":   
                    cursor.execute('INSERT INTO quizapp_answer (uid, created_at, updated_at,answer,is_correct,question_id) VALUES (?, ?, ?, ?, ?, ?)', (answer_id, created_at, updated_at,answer,is_correct,question_id))
                    conn.commit()
              else:
                    print (answer_id, created_at, updated_at,answer,is_correct,question_id)
          
            else:    
            # Iterate through List OptionsText and get corresponding values from List OptionsTrue
              for a_option in optionstext:
                answer_id = generate_uuid()
 
                is_correct = lookup_dict.get(a_option) 
                """
                if question['type']=="true_false":
                   print("a_option is ", a_option)
                   print("Is_Correct is ", is_correct)
                   """
                if dryrun=="No":   
                    cursor.execute('INSERT INTO quizapp_answer (uid, created_at, updated_at,answer,is_correct,question_id) VALUES (?, ?, ?, ?, ?, ?)', (answer_id, created_at, updated_at,a_option,is_correct,question_id))
                    conn.commit()
                else:
                    print (answer_id, created_at, updated_at,a_option,is_correct,question_id)
          
             
         
            
if __name__ == '__main__':
    main()
