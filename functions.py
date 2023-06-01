import sqlite3
import datetime
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

def into_sql(type, year, mark, id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT v_level FROM marks WHERE id={id[0][0]} AND year="{year}"')
    if len(cursor.fetchall()) != 0:
        cursor.execute(f'''UPDATE marks SET {type}="{mark}" WHERE id={id[0][0]} AND year="{year}"''')
    else:
        cursor.execute(f'''INSERT INTO marks(id,year,{type}) VALUES({id[0][0]}, "{year}", "{mark}")''')
    conn.commit()
    pass

def get_id(name,clas):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT id FROM students WHERE name="{name}" AND class={clas}')
    return cursor.fetchall()

def get_name(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT name, class, english_level, group_num, olympiads FROM students WHERE id={id}')
    return list(cursor.fetchall())

def profile(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    sp=[]
    #['year', 'v_level', 'v_ball', 't_one', 't_two', 't_tree', 'year_mark', 'winter', 'summer', 'test_oge']

    sp2=[]
    cursor.execute(f'SELECT year FROM marks WHERE id={id}')
    for i in list(cursor.fetchall()):
        if i[0] not in sp2:
            sp2.append(i[0])
    for i in sp2:
        q={}
        cursor.execute(f'''SELECT v_level, v_ball, t_one, t_two, t_three, year_mark, winter, summer, test_oge FROM marks WHERE year='{i}' AND id={id}''')
        o = list(cursor.fetchall())
        print(11111)
        q['year'] = i
        q['v_level'] = o[0][0]
        q['v_ball'] = o[0][1]
        q['t_one'] = o[0][2]
        q['t_two'] = o[0][3]
        q['t_three'] = o[0][4]
        q['year_mark'] = o[0][5]
        q['winter'] = o[0][6]
        q['summer'] = o[0][7]
        q['test_oge'] = o[0][8]
        sp.append(q)
    return sp

