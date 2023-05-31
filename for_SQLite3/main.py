import sqlite3
conn = sqlite3.connect(r"data.db")
cur = conn.cursor()
#cur.execute(f"CREATE TABLE class{classn} (name TEXT);")
c=180
class1 = open('class.txt', encoding="utf8").readlines()
for i in class1:
    cur.execute(f"""INSERT INTO students VALUES (11, {c}, "{' '.join(i.split())}");""")
    #cur.execute(f"""UPDATE students SET id = {c} WHERE name = '{' '.join(i.split())}';""")
    c+=1
conn.commit()
