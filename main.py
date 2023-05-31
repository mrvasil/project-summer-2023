from flask import Flask, render_template, request, redirect
import sqlite3
import hashlib
import secretsq
from datetime import datetime
app = Flask(__name__)


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



@app.route('/')
def index():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        return redirect("/students", code=302)
    elif user == 'successfully_student':
        return redirect("/students", code=302)
    else:
        return render_template('index.html')


@app.route('/students')
def students():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        return render_template('students_for_1.html', data=names())
    elif user == 'successfully_student':
        return render_template('students_for_2.html', data=names())
    else:
        return redirect("/", code=302)


@app.route('/profile')
def profile():
    name = request.args.get('name')
    class1 = request.args.get('class')
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        return "Имя: "+name+"<br>Класс: "+class1
    elif user == 'successfully_student':
        return "Имя: "+name+"<br>Класс: "+class1
    else:
        return redirect("/", code=302)

@app.route('/check_password', methods=['POST'])
def check_password():   
    password = request.form['password']
    if hashlib.sha1(password.encode()).hexdigest() == secretsq.pass1:
        return secretsq.secret_cookie
    else:
        return 'Неверный пароль'
    



cyear = datetime.now().year
Dict = {'v': 'Входное тестирование', 't1': '1 триместр', 't2': '2 триместр', 't3': '3 триместр','s1': 'Зимняя сессия', 's2': 'Летняя сессия'}
Dict2 = {'y1': cyear, 'y2': cyear - 1, 'y3': cyear - 2}

def into_sql(type, year, mark, id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    print(id[0][0], mark, year, type)
    cursor.execute(f'''INSERT INTO marks(id,mark,year,type) VALUES({id[0][0]}, {mark}, {year}, "{type}")''')
    conn.commit()
    pass

def get_id(name,clas):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT id FROM students WHERE name="{name}" AND class={clas}')
    return cursor.fetchall()


@app.route('/newmark')
def newmark():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        name = request.args.get('name')
        clas = request.args.get('class')
        return render_template('newmark.html', name = name, grade = clas, year1 = cyear, year2 = cyear - 1, year3 = cyear - 2)

@app.route('/addmark', methods = ['POST', 'GET'])
def addmark():
    mark = request.form['mark']
    type = Dict[request.form.get('type')]
    year = Dict2[request.form.get('year')]
    name = request.args.get('name')
    clas = request.args.get('class')
    id = get_id(name, clas)
    into_sql(type, year, mark, id)
    print(name, clas, year)
    return redirect(f'/profile?name={name}&class={clas}', 302)


    


app.run(port=9127, host='0.0.0.0', debug=True)