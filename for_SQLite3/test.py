import sqlite3
conn = sqlite3.connect(r"data.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM students")
names=cursor.fetchall()
for i in range(len(names)):
    cursor.execute(f"""UPDATE students SET id = {i} WHERE name = '{names[i][0]}';""")

conn.commit()