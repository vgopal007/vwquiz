import sqlite3
dbname="db.sqlite3"
dbname=input("Database Name? ").strip()

# Connect to the database
conn = sqlite3.connect(dbname)
cursor = conn.cursor()

dryrun= input("Dry run?  Yes for display only, No to subject data into the database : Yes/No : ")
 

try:
    delete_query = f"DELETE FROM quizapp_UserResponse"
    cursor.execute(delete_query)
    delete_query = f"DELETE FROM quizapp_UserSession"
    cursor.execute(delete_query)
    conn.commit()
except:
    print("QuizSession/UserResponse not found")

print("Tables truncated")
      
    

# Close the database connection
conn.close()