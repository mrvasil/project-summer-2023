import sqlite3
def names():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    sp=[]
    qn = ["five", "six", "seven", "eight", "nine", "ten", "eleven"]
    for i in range(5, 12):
        cursor.execute("SELECT name FROM students WHERE class="+str(i))
        names = list(cursor.fetchall())
        for j in range(len(names)):
            if len(sp)<j+1:
                sp.append({})
            sp[j][qn[i-5]] = names[j][0]
    conn.close()
    return sp
print(names())