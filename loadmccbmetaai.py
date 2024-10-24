# question_type can be RB for 1 answer RB, CB, IN
import sqlite3
import json
import uuid
import random
import re
# import custom functions from vwquizfunclib.py
from  vwquizfunclib import select_category
from  vwquizfunclib import strip_non_alphanumeric_leading
from  vwquizfunclib import strip_non_alphanumeric



# Assumes this prefix or suffix on every question line in the question bank sourced from Meta AI
prefixq = "_"
suffixq = "?" 
# Assumes this prefix on the second and every other even number line
prefixa1 = "Answer"
#prefixa2 = "Answer: "

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('vwquiz.db')
cursor = conn.cursor()
# Enable foreign key constraints, not ON by default!
cursor.execute("PRAGMA foreign_keys = ON;")

# Open the text file
filename = input ("Enter the filename of the multiple choice Question Set from Meta AI :")

try:
 with open(filename, 'r' ,encoding='utf-8') as file:
  lines = file.readlines()
except UnicodeDecodeError as e:
  print(f"Error decoding file: {e}")

# Retrieve the list of categories from the quizapp_types table 
cursor.execute('SELECT gfg_name FROM quizapp_types')
categories = [row[0] for row in cursor.fetchall()]

cat = select_category(categories) # ask user to select a category



# from django.db import models
from datetime import datetime
from datetime import date


created_at = date.today()
updated_at = date.today()

cursor.execute("SELECT uid, gfg_name FROM quizapp_types where gfg_name=?", (cat,))

rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Category: {row[1]}")
    gfg_id= row[0]

gfg_id = str(gfg_id).replace('-', '')
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

# Process the lines and insert into the database
for i in range(0, len(lines), 1):
    line=lines[i].strip()  
    answerline=False
    line = strip_non_alphanumeric_leading(line)
    line = line.strip()
    if (len(line) < 2 ):
       continue
    if (suffixq in line):
       question=line
       q=q+1
       options=[]
       optionstext=[]
       optionstrue=[]
    elif line[1] == ")":
       options.append(line[0])        
       optionstext.append(line[3:])
    elif prefixa1 in line:
       answer = line[len(prefixa1):].strip()  # get remainder of string after Answer
       answer = strip_non_alphanumeric(answer)  
       answers = answer.strip(" ")
       answerline=True
#    elif line.startswith(prefixa2):
#       answer = line[len(prefixa2):].strip()
#       answerline=True
    elif line.startswith("Exit"):
       break
    else:
       cat=line
 
    if (answerline):
        answer_list=[]
        for answer in answers:
            answer=strip_non_alphanumeric(answer)
            if len(answer)==1: answer_list.append(answer)
            
 #       optionstrue = [x==answer for x in options]
        optionstrue = [x in answer_list for x in options]

        question_id = uuid.uuid4()
        question_id = str(question_id).replace('-', '')
        print("Question : ", question)
        print(question_id, created_at, updated_at,"CB", question,cat, 1, gfg_id)
    
        cursor.execute('INSERT INTO quizapp_question (uid, created_at, updated_at, question_type, question, topic, marks,answer_explanation, gfg_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (question_id, created_at, updated_at,"CB", question,cat, 1,"", gfg_id))
        conn.commit()
        lookup_dict = dict(zip(optionstext, optionstrue))

# Iterate through List OptionsText and get corresponding values from List OptionsTrue
        for a_option in optionstext:
            answer_id = uuid.uuid4()
            answer_id = str(answer_id).replace('-', '')
            is_correct = lookup_dict.get(a_option) 
            cursor.execute('INSERT INTO quizapp_answer (uid, created_at, updated_at,answer,is_correct,question_id) VALUES (?, ?, ?, ?, ?, ?)', (answer_id, created_at, updated_at,a_option,is_correct,question_id))
            conn.commit()
            print (answer_id, created_at, updated_at,a_option,is_correct,question_id)

        print("Answer : ", answer_list)


else:
    print ("Number of questions added - "+ str(q))


# Query to join question and answer tables
#cursor.execute('''
#SELECT quizapp_answer.answer, quizapp_question.question
#FROM 
#quizapp_answer
#JOIN quizapp_question ON quizapp_answer.question_id = quizapp_question.uid
#''')

conn.close()
