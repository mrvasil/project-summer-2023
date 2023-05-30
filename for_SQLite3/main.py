import sqlite3
conn = sqlite3.connect(r"data.db")
cur = conn.cursor()
classn=input()
cur.execute(f"CREATE TABLE class{classn} (name TEXT);")
class1 = open('class.txt', encoding="utf8").readlines()
for i in class1:
    cur.execute(f"""INSERT INTO class{classn} VALUES ("{' '.join(i.split())}");""")
conn.commit()
