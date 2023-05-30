import sqlite3
conn = sqlite3.connect(r"data.db")
cursor = conn.cursor()
for i in range(5, 12):
    cursor.execute("SELECT name FROM class"+str(i))
    names = list(cursor.fetchall())
    for j in range(len(names)):
        cursor.execute(f"""UPDATE class{i} SET user_id = {j} WHERE name = '{names[j][0]}';""")

conn.commit()