from flask import Flask, render_template, request, redirect
import sqlite3
import hashlib
import secretsq
import functions
from datetime import datetime
app = Flask(__name__)




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
        return render_template('students_for_1.html', data=functions.names())
    elif user == 'successfully_student':
        return render_template('students_for_2.html', data=functions.names())
    else:
        return redirect("/", code=302)


@app.route('/profile')
def profile():
    name = request.args.get('name')
    class1 = request.args.get('class')
    user = request.cookies.get('user')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT english_level, group_num, id FROM students WHERE name="{name}" AND class={class1}')
    output = list(cursor.fetchall())
    english_level = output[0][0]
    group = output[0][1]
    id = output[0][2]
    if user == secretsq.secret_cookie:
        return render_template('profile_1.html', name=name, class1=class1, english_level=english_level, group=group, id=id)
    elif user == 'successfully_student':
        return render_template('profile_2.html', name=name, class1=class1, english_level=english_level, group=group)
    else:
        return redirect("/", code=302)


@app.route('/check_password', methods=['POST'])
def check_password():   
    password = request.form['password']
    if hashlib.sha1(password.encode()).hexdigest() == secretsq.pass1:
        return secretsq.secret_cookie
    else:
        return 'Неверный пароль'
    

@app.route('/change_profile')
def change_profile():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        id = request.args.get('id')
        return render_template('change_profile.html')
    else:
        return redirect("/", code=302)




@app.route('/newmark')
def newmark():
    user = request.cookies.get('user')
    cyear = datetime.now().year
    if user == secretsq.secret_cookie:
        name = request.args.get('name')
        clas = request.args.get('class')
        return render_template('newmark.html', name = name, grade = clas, year0 = cyear + 1, year1 = cyear, year2 = cyear - 1, year3 = cyear - 2)
    else:
        return redirect("/", code=302)

@app.route('/addmark', methods = ['POST', 'GET'])
def addmark():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        cyear = datetime.now().year
        Dict = {'v': 'Входное тестирование', 't1': '1 триместр', 't2': '2 триместр', 't3': '3 триместр','s1': 'Зимняя сессия', 's2': 'Летняя сессия'}
        Dict2 = {'y1': f'{cyear} - {cyear+1}', 'y2': f'{cyear-1} - {cyear}', 'y3': f'{cyear-2} - {cyear-1}'}
        mark = request.form['mark']
        type = Dict[request.form.get('type')]
        year = Dict2[request.form.get('year')]
        name = request.args.get('name')
        clas = request.args.get('class')
        id = functions.get_id(name, clas)
        functions.into_sql(type, year, mark, id)
        print(name, clas, year)
        return redirect(f'/profile?name={name}&class={clas}', 302)
    else:
        return redirect("/", code=302)

    


app.run(port=9127, host='0.0.0.0', debug=True)