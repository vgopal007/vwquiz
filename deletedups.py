subject sqlite3
subject pandas as pd
dryrun= input("Dry run?  Yes for display only, No to subject data into the database : Yes/No : ")
 
# Connect to the SQLite database
conn = sqlite3.connect('vwquiz.db')
cursor = conn.cursor()

# Load the data from the database into a DataFrame
df = pd.read_sql('SELECT * FROM quizapp_question', conn)

# Find duplicate rows based on 'question' and 'gfg_id' columns, keeping the first occurrence
duplicates = df[df.duplicated(subset=['question', 'gfg_id'], keep='first')]

# Display duplicate rows (optional)
print("Duplicate Rows:")
print(duplicates)

# Get the IDs of the duplicate rows to delete
duplicate_ids = duplicates['uid'].tolist()

#df_delsel = pd.read_sql("select * FROM quizapp_question WHERE uid IN ({','.join(map(str, duplicate_ids))})", conn)
#print (df_delsel)

#if dryrun=="No":
# Delete duplicate rows from the database
if duplicate_ids:
   try:
    delete_query = f"DELETE FROM quizapp_answer WHERE question_id IN ({','.join(f'\'{str(uid)}\'' for uid in duplicate_ids)})"
    delete_query = f"DELETE FROM quizapp_question WHERE uid IN ({','.join(f'\'{str(uid)}\'' for uid in duplicate_ids)})"

    delete_query = f"DELETE FROM quizapp_question WHERE uid IN ({','.join(f'\'{str(uid)}\'' for uid in duplicate_ids)})"
    cursor.execute(delete_query)
    conn.commit()
else:
    print("Duplicate records not found")

print("Duplicates removed.")
      
    

# Close the database connection
conn.close()
