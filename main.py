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
    group = str(request.args.get('group'))
    #group='A'
    if user == secretsq.secret_cookie:
        return render_template('students_for_1.html', data=functions.names(group))
    elif user == 'successfully_student':
        return render_template('students_for_2.html', data=functions.names(group))
    else:
        return redirect("/", code=302)


@app.route('/profile')
def profile():
    name = request.args.get('name')
    class1 = request.args.get('class')
    user = request.cookies.get('user')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT english_level, group_num, id, olympiads, teacher_name FROM students WHERE name="{name}" AND class={class1}')
    output = list(cursor.fetchall())
    english_level = str(output[0][0]).replace('None', '')
    group = str(output[0][1]).replace('None', '')
    id = output[0][2]
    olympiads = str(output[0][3]).replace('None', '')
    teacher_name = str(output[0][4]).replace('None', '')

    data=functions.profile(id)

    old_x = ['Входной тест (Уровень)', 'Входной тест (Балл)', 'Триместр 1', 'Триместр 2', 'Триместр 3', 'Годовая', 'Зимняя сессия', 'Летняя сессия']
    old_y = list(data[0].values())[1:-2]
    x = []
    y = []
    for i, j in zip(old_x, old_y):
        if j != '':
            x.append(i)
            y.append(j)
    if user == secretsq.secret_cookie:
        return render_template('profile_1.html', name=name, class1=class1, english_level=english_level, group=group, id=id, olympiads=olympiads, teacher_name=teacher_name, data=data, max_i=data[-1]["i"], status=str(request.args.get('status')).replace('None', ''), graph_x=x, graph_y=y, graph_x_=["1"], graph_y_=[1])
    elif user == 'successfully_student':
        return render_template('profile_2.html', name=name, class1=class1, english_level=english_level, group=group, olympiads=olympiads, teacher_name=teacher_name, data=data, graph_x=x, graph_y=y)
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
        return render_template('change_profile.html', name=str(out[0][0]).replace('None', ''), class1=str(out[0][1]).replace('None', ''), english_level=str(out[0][2]).replace('None', ''), group=str(out[0][3]).replace('None', ''), olympiads=str(out[0][4]).replace('None', ''), teacher_name=str(out[0][5]).replace('None', ''), id=id)
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
        teacher_name = request.form['teacher_name']
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute(f'''UPDATE students SET name='{name}', class={class1}, english_level='{english_level}', group_num='{group}', olympiads='{olympiads}', teacher_name="{teacher_name}" WHERE id={id};''')
        conn.commit()
        functions.backup()
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
        functions.backup()
        return redirect(f'/students', code=302)
    else:
        return redirect("/", code=302)
    
@app.route('/marks', methods = ['POST', 'GET'])
def marks():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        id = request.args.get('id')
        name = request.args.get('name')
        class1 = request.args.get('class')
        max_i = request.args.get('max_i')
        for i in range(0, int(max_i)+1):
            year = request.form['year'+str(i)]
            v_level = request.form['v_level'+str(i)]
            v_ball = request.form['v_ball'+str(i)]
            t_one = request.form['t_one'+str(i)]
            t_two = request.form['t_two'+str(i)]
            t_three = request.form['t_three'+str(i)]
            year_mark = request.form['year_mark'+str(i)]
            winter = request.form['winter'+str(i)]
            summer = request.form['summer'+str(i)]
            test_oge = request.form['test_oge'+str(i)]

            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute(f'''UPDATE marks SET v_level='{v_level}', v_ball='{v_ball}', t_one='{t_one}', t_two='{t_two}', t_three='{t_three}', year_mark='{year_mark}', winter='{winter}', summer='{summer}', test_oge='{test_oge}' WHERE id={id} AND year='{year}';''')
        
            conn.commit()
            functions.backup()

        return redirect(f'/profile?name={name}&class={class1}&status=Успешно', code=302)
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
        Dict2 = {'y1': f'{cyear}-{cyear+1}', 'y2': f'{cyear-1}-{cyear}', 'y3': f'{cyear-2}-{cyear-1}'}
        ms = ['v_level', 'v_ball', 't_one', 't_two', 't_tHree', 'winter', 'summer', 'test_oge', 'year_mark']
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
        functions.backup()
        return redirect(f'/change_profile?id={nid}', 302)
    else:
        return redirect(f'/', code=302)

    

    


app.run(port=9127, host='0.0.0.0', debug=True)