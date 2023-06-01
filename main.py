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
    cursor.execute(f'SELECT english_level, group_num, id, olympiads FROM students WHERE name="{name}" AND class={class1}')
    output = list(cursor.fetchall())
    english_level = output[0][0]
    group = output[0][1]
    id = output[0][2]
    olympiads = output[0][3]

    data=functions.profile(id)
    if user == secretsq.secret_cookie:
        return render_template('profile_1.html', name=name, class1=class1, english_level=english_level, group=group, id=id, olympiads=olympiads, data=data)
    elif user == 'successfully_student':
        return render_template('profile_2.html', name=name, class1=class1, english_level=english_level, group=group, olympiads=olympiads)
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
        out = functions.get_name(id)
        print(out[0][0], out[0][1], out[0][2], out[0][3], out[0][4])
        return render_template('change_profile.html', name=out[0][0], class1=out[0][1], english_level=out[0][2], group=out[0][3], olympiads=out[0][4], id=id)
    else:
        return redirect("/", code=302)
    
@app.route('/change_profile2', methods = ['POST', 'GET'])
def change_profile2():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        id = request.args.get('id')
        name = request.form['name']
        class1 = request.form['class1']
        english_level = request.form['level']
        group = request.form['group']
        olympiads = request.form['olympiads']
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute(f'''UPDATE students SET name='{name}', class={class1}, english_level='{english_level}', group_num='{group}', olympiads='{olympiads}' WHERE id={id};''')
        conn.commit()
        return redirect(f'/profile?name={name}&class={class1}', code=302)
    else:
        return redirect("/", code=302)


@app.route('/del_user')
def del_user():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        id = request.args.get('id')
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor() 
        cursor.execute(f'''DELETE FROM students WHERE id={id};''')
        conn.commit()
        return redirect(f'/students', code=302)
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
        Dict = {'vb': 'Входное тестирование балл', 'vl': 'Входное тестирование уровень', 't1': '1 триместр', 't2': '2 триместр', 't3': '3 триместр','s1': 'Зимняя сессия', 's2': 'Летняя сессия', 'oge': 'Пробник ОГЭ', 'y': 'Годовая'}
        Dict2 = {'y1': f'{cyear} - {cyear+1}', 'y2': f'{cyear-1} - {cyear}', 'y3': f'{cyear-2} - {cyear-1}'}
        ms = ['v_level', 'v_ball', 't_one', 't_two', 't_tree', 'winter', 'summer', 'test_oge', 'year_mark']
        Dict3 = dict(zip(list(Dict.keys()), ms))
        mark = request.form['mark']
        type = Dict3[request.form.get('type')]
        year = Dict2[request.form.get('year')]
        name = request.args.get('name')
        clas = request.args.get('class')
        id = functions.get_id(name, clas)
        functions.into_sql(type, year, mark, id)
        return redirect(f'/profile?name={name}&class={clas}', 302)
    else:
        return redirect("/", code=302)
    
@app.route('/addstudent')
def new_id():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute(f'''SELECT MAX(id) FROM students;''')
        for row in cursor:
            for elem in row:
                nid = elem
        nid += 1
        cursor.execute(f'''INSERT INTO students (id) VALUES ({nid});''')
        conn.commit()
        return redirect(f'/change_profile?id={nid}', 302)
    else:
        return redirect(f'/', code=302)

    

    


app.run(port=9127, host='0.0.0.0', debug=True)