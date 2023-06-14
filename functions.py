import sqlite3
import datetime
import shutil
import os
def names(group, search):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    sp=[]
    qn = ["five", "six", "seven", "eight", "nine", "ten", "eleven"]
    for i in range(5, 12):
        if group != 'None':
            cursor.execute(f"""SELECT name FROM students WHERE class={i} AND group_num="{group}" AND name LIKE '%{search}%'""")
        else:
            cursor.execute(f"SELECT name FROM students WHERE class={i} AND name LIKE '%{search}%'")
        names = sorted(list(cursor.fetchall()))
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
    backup()
    pass

def get_id(name,clas):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT id FROM students WHERE name="{name}" AND class={clas}')
    return cursor.fetchall()

def get_name(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT name, class, english_level, group_num, olympiads, teacher_name FROM students WHERE id={id}')
    return list(cursor.fetchall())

def profile(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    sp=[]
    sp2=[]
    cursor.execute(f'SELECT year FROM marks WHERE id={id}')
    #sp2.append(now_year())
    for i in list(cursor.fetchall()):
        if (i[0] not in sp2):
            sp2.append(i[0])
    if now_year() not in sp2:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO marks(id, year) VALUES({id}, "{now_year()}")')
        conn.commit()
        backup()
        sp.append({'year': now_year(), 'v_level': '0', 'v_ball': '0', 't_one': '0', 'winter': '0', 't_two': '0', 't_three': '', 'year_mark': '0', 'summer': '0', 'test_oge': '0', 'i': 0})
    for i in sp2:
        q={}
        cursor.execute(f'''SELECT v_level, v_ball, t_one, winter, t_two, t_three, year_mark, summer, test_oge FROM marks WHERE year='{i}' AND id={id}''')
        o = list(cursor.fetchall())
        q['year'] = i
        q['v_level'] = str(o[0][0]).replace('None', '0')
        q['v_ball'] = str(o[0][1]).replace('None', '0')
        q['t_one'] = str(o[0][2]).replace('None', '0')
        q['winter'] = str(o[0][3]).replace('None', '0')
        q['t_two'] = str(o[0][4]).replace('None', '0')
        q['t_three'] = str(o[0][5]).replace('None', '0')
        q['year_mark'] = str(o[0][6]).replace('None', '0')
        q['summer'] = str(o[0][7]).replace('None', '0')
        q['test_oge'] = str(o[0][8]).replace('None', '0')
        q['i'] = sp2.index(i)
        for i in ['v_level', 'v_ball', 't_one', 'winter', 't_two', 't_three', 'year_mark', 'summer', 'test_oge']:
            if q[i]=='':
                q[i]='0'
        sp.append(q)
    return sp

def now_year():
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    if month < 9:
        return f"{year-1}-{year}"
    else:
        return f"{year}-{year+1}"
    
def backup():
    sp = os.listdir('db_backup/')
    sp2 = []
    for i in sp:
        sp2.append(int(i[:-3]))
    c = sum([len(files) for r, d, files in os.walk("db_backup/")])
    shutil.copyfile('data.db', f'db_backup/{c+1+min(sp2)}.db')
    if c>=30:
        os.remove('db_backup/'+str(min(sp2))+'.db')


def cancel_backup():
    sp = os.listdir('db_backup/')
    sp2 = []
    for i in sp:
        sp2.append(int(i[:-3]))
    shutil.copyfile(f'db_backup/{max(sp2)-1}.db', 'data.db')
    os.remove(f'db_backup/{max(sp2)}.db')
    
#graph уже не используется
def graph(data):
    d = {'v_ball': 'Входной тест (Уровень)', 'v_level': 'Входной тест (Балл)', 't_one': 'Триместр 1', 'winter': 'Зимняя сессия', 't_two': 'Триместр 2', 't_three': 'Триместр 3', 'year': 'Годовая', 'summer': 'Летняя сессия'}
    old_x = ['Входной тест (Уровень)', 'Входной тест (Балл)', 'Триместр 1', 'Зимняя сессия', 'Триместр 2', 'Триместр 3', 'Годовая', 'Летняя сессия']
    old_y = list(data.values())[1:-2]
    x = []
    y = []
    for i, j in zip(old_x, old_y):
        if j != '':
            x.append(i)
            y.append(j)
    
    return [x, y]


def middle_of_group(class1, group):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    names=['v_ball', 't_one', 'winter', 't_two', 't_three', 'year_mark', 'summer']
    sp = []
    for i in names:
        cursor.execute(f'SELECT avg({i}) FROM marks WHERE id=(SELECT id FROM students WHERE class={class1} AND group_num="{group}") AND year="{now_year()}"')
        sp.append(list(cursor.fetchall())[0][0])

    return sp














def groups(param, clas):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    old_y = []
    ny = now_year()
    ms = ['v_ball', 't_one', 'winter', 't_two', 't_three', 'year_mark', 'summer']
    for i in ms:
        select = f'''SELECT AVG(m.{i}) FROM marks m
            JOIN students s ON s.id = m.id
            WHERE s.class={clas} {param} AND m.{i} > 0 AND m.year="{ny}";'''
        #print(select)
        cursor.execute(select)
        old_y.append(cursor.fetchall()[0][0])
    return old_y
