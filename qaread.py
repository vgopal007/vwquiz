# Open the text file
with open('questionbank.txt', 'r') as file:
    lines = file.readlines()

# Process the lines and insert into the database
for i in range(0, len(lines), 2):
    question = lines[i].strip()
    answer = lines[i+1].strip()
    cursor.execute('INSERT INTO qa (question, answer) VALUES (?, ?)', (question, answer))

conn.commit()
conn.close()# Open the text file
with open('qa.txt', 'r') as file:
    lines = file.readlines()

# Process the lines and insert into the database
for i in range(0, len(lines), 2):
    question = lines[i].strip()
    answer = lines[i+1].strip()
    cursor.execute('INSERT INTO qa (question, answer) VALUES (?, ?)', (question, answer))

conn.commit()
conn.close()

