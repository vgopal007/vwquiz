import sqlite3
from datetime import date

def connect_db(db_name='vwquiz.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    return conn, cursor

def close_db(conn):
    conn.commit()
    conn.close()

def fetch_categories(cursor):
    cursor.execute('SELECT subject_name FROM quizapp_types')
    return [row[0] for row in cursor.fetchall()]

def fetch_subject_id(cursor, category):
    cursor.execute("SELECT uid, subject_name FROM quizapp_types WHERE subject_name=?", (category,))
    rows = cursor.fetchall()
    if rows:
        return rows[0][0]
    return None

def insert_question(cursor, question_data):
    cursor.execute('''
        INSERT INTO quizapp_question (
            uid, created_at, updated_at, question_type, question, topic_id, marks,
            answer_explanation, difficulty_level, reference, source, subject_id, delete_flag, qc_passed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', question_data)

def insert_topic(cursor, topic_data):
    cursor.execute('''
        INSERT INTO quizapp_topics (
            uid, created_at, updated_at, topic, subject_id, weight_perc, delete_flag
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', topic_data)
        