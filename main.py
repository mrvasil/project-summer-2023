from flask import *
import sqlite3
import hashlib
import secretsq
import functions
from datetime import datetime
from werkzeug.exceptions import BadRequest
import random
import os
import re

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
    search = str(request.args.get('search')).replace('None', '')
    if user == secretsq.secret_cookie:
        return render_template('students_for_1.html', data=functions.names(group, search))
    elif user == 'successfully_student':
        cookie = str(request.cookies.get('id'))
        if cookie != 'None':
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            cursor.execute(f'SELECT name, class FROM students WHERE id=(?)', (cookie,))
            out = list(cursor.fetchall())
            return render_template('students_for_2.html', data=functions.names(group, search), name=out[0][0], class1=out[0][1])
        else:
            return render_template('students_for_2.html', data=functions.names(group, search))
    else:
        return redirect("/", code=302)


@app.route('/profile')
def profile():
    name = request.args.get('name')
    class1 = request.args.get('class')
    user = request.cookies.get('user')

    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT english_level, group_num, id, olympiads, teacher_name FROM students WHERE name=(?) AND class=(?)', (name, class1,))
    output = list(cursor.fetchall())
    english_level = str(output[0][0]).replace('None', '')
    group = str(output[0][1]).replace('None', '')
    id = output[0][2]
    olympiads = str(output[0][3]).replace('None', '')
    teacher_name = str(output[0][4]).replace('None', '')

    data = functions.profile(id)

    graphs_y = []
    years = []
    graph_x =  ['Входной тест (Балл)', 'Триместр 1', 'Зимняя сессия', 'Триместр 2', 'Триместр 3', 'Годовая', 'Летняя сессия']
    for i in range(len(data)):
        graph = functions.graph(data[i])
        graph[0]=graph[0][1:]
        graph[1]=graph[1][1:]
        graphs_y.append(graph[1])
        years.append(data[i]['year'])
    for j in data:
        for i in ['v_level', 'v_ball', 't_one', 'winter', 't_two', 't_three', 'year_mark', 'summer', 'test_oge']:
            if j[i]=='0':
                j[i]=''



    if user == secretsq.secret_cookie:
        return render_template('profile_1.html', name=name, class1=class1, english_level=english_level, group=group, id=id, olympiads=olympiads, teacher_name=teacher_name, data=data, max_i=data[-1]["i"], status=str(request.args.get('status')).replace('None', ''),
                               graph_x=graph_x,
                               graphs_y=graphs_y,
                               years=years,
                               middle_of_group=functions.middle_of_group(class1, group),
                               colors=[f'rgb({random.randint(0,190)}, {random.randint(0,190)}, {random.randint(0,190)})' for _ in range(len(years)+1)]
                               )
    elif user == 'successfully_student':
        return render_template('profile_2.html', name=name, class1=class1, english_level=english_level, group=group, olympiads=olympiads, teacher_name=teacher_name, id=id, data=data,
                               graph_x=graph_x,
                               graphs_y=graphs_y,
                               years=years,
                               middle_of_group=functions.middle_of_group(class1, group),
                               colors=[f'rgb({random.randint(0,190)}, {random.randint(0,190)}, {random.randint(0,190)})' for _ in range(len(years)+1)]
                               )
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
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        #cursor.execute(f'''UPDATE students SET name='{name}', class={class1}, english_level='{english_level}', group_num='{group}', olympiads='{olympiads}', teacher_name="{teacher_name}" WHERE id={id};''')
        cursor.execute('''UPDATE students SET name=(?), class=(?), english_level=(?), group_num=(?), olympiads=(?), teacher_name=(?)  WHERE id=(?);''', (name,class1,english_level,group,olympiads,teacher_name,id,))
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
        conn = sqlite3.connect('data/data.db')
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
            winter = request.form['winter'+str(i)]
            t_two = request.form['t_two'+str(i)]
            t_three = request.form['t_three'+str(i)]
            year_mark = request.form['year_mark'+str(i)]
            summer = request.form['summer'+str(i)]
            test_oge = request.form['test_oge'+str(i)]
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            if v_level != '':
                cursor.execute(f'''UPDATE students SET english_level='{v_level}' WHERE id="{id}";''')
            cursor.execute(f'''UPDATE marks SET v_level='{v_level}', v_ball='{v_ball}', t_one='{t_one}', winter='{winter}', t_two='{t_two}', t_three='{t_three}', year_mark='{year_mark}', summer='{summer}', test_oge='{test_oge}' WHERE id={id} AND year='{year}';''')
            conn.commit()
            functions.backup()

        return redirect(f'/profile?name={name}&class={class1}&status=Успешно', code=302)
    else:
        return redirect("/", code=302)



@app.route('/cancel_backup')
def cancel_backup():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        functions.cancel_backup()
        return redirect(f'/students', code=302)
    else:
        return redirect("/", code=302)
    

@app.route('/logs')
def logs():
    user = request.cookies.get('user')
    if (user == secretsq.secret_cookie) and (request.args.get('p') == secretsq.admin_key):
        result = "<br>".join(open("logs.txt", "r").readlines())
        return re.sub(r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))', '', result)
    else:
        return redirect("/", code=302)


@app.errorhandler(500)
def handle_bad_request(e):
    return '<center><h1>Хммм... Странно, произошла какая-то ошибка. Расскажите об этом на странцие <a href="/help">/help</a></h1></center>', 500

@app.errorhandler(404)
def handle_not_found(e):
    return '<center><h1>Хммм... Странно, такой странички нет(. Если Вы думаете что она должна существовать, расскажите об этом на странцие <a href="/help">/help</a></h1></center>', 404

@app.route('/admin')
def admin():
    return "Hello, CTFer!)"

@app.route('/help')
def help():
    return redirect("https://t.me/mrvasil", 302)






@app.route('/newmark')
def newmark():
    user = request.cookies.get('user')
    cyear = int(functions.now_year()[:4])
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
        cyear = int(functions.now_year()[:4])
        Dict = {'vb': 'Входное тестирование балл', 'vl': 'Входное тестирование уровень', 't1': '1 триместр', 't2': '2 триместр', 't3': '3 триместр','s1': 'Зимняя сессия', 's2': 'Летняя сессия', 'oge': 'Пробник ОГЭ', 'y': 'Годовая'}
        Dict2 = {'y1': f'{cyear}-{cyear+1}', 'y2': f'{cyear-1}-{cyear}', 'y3': f'{cyear-2}-{cyear-1}'}
        ms = ['v_ball', 'v_level', 't_one', 't_two', 't_three', 'winter', 'summer', 'test_oge', 'year_mark']
        Dict3 = dict(zip(list(Dict.keys()), ms))
        mark = request.form['mark']
        type = Dict3[request.form.get('type')]
        year = Dict2[request.form.get('year')]
        name = request.args.get('name')
        clas = request.args.get('class')
        id = functions.get_id(name, clas)
        if type == 't_one' or type == 't_two' or type == 't_three' or type == 'year_mark':
            if not mark.isdigit():
                return redirect(f'/profile?name={name}&class={clas}&status=Введена неправильная оценка', 302)
            if not (0 < int(mark) < 11):
                return redirect(f'/profile?name={name}&class={clas}&status=Введена неправильная оценка', 302)
        if type == 'v_level':
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            cursor.execute(
                f'''UPDATE students SET english_level='{mark}' WHERE id="{id[0][0]}";''')
            conn.commit()
            functions.backup()
        functions.into_sql(type, year, mark, id)
        return redirect(f'/profile?name={name}&class={clas}', 302)
    else:
        return redirect("/", code=302)
    
@app.route('/addstudent')
def new_id():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        conn = sqlite3.connect('data/data.db')
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
    

    


@app.route('/class')
def class_graph():
    user = request.cookies.get('user')
    if (user == secretsq.secret_cookie) or (user == 'successfully_student'):
        clas = request.args.get('grade')
        old_x = ['Входной тест (Балл)', 'Триместр 1', 'Зимняя сессия', 'Триместр 2', 'Триместр 3',
                 'Годовая', 'Летняя сессия']
        ms = ['v_ball', 't_one', 'winter', 't_two', 't_three', 'year_mark', 'summer' ]
        ms2 = [' ', ' AND s.group_num="A"', ' AND s.group_num="B"', ' AND s.group_num="C"', ' AND s.group_num="D"']
        msy = []
        x1 = ''
        for ii in ms2:
            old_y = functions.groups(ii, clas)
            x = []
            if ii == ' ':
                x1 = x
            y = []
            for i, j in zip(old_x, old_y):
                if j == None:
                    x.append(i)
                    y.append(0)
                if (j != '') and (j != None):
                    x.append(i)
                    y.append(j)
            msy.append(y)
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute(f'''SELECT count(name) FROM students WHERE class=(?)''', (clas,))
        students = cursor.fetchall()[0][0]  
        cursor.execute(f'''SELECT count(name) FROM students WHERE group_num="A" AND class=(?)''', (clas,))
        groupA = cursor.fetchall()[0][0]
        cursor.execute(f'''SELECT count(name) FROM students WHERE group_num="B" AND class=(?)''', (clas,))
        groupB = cursor.fetchall()[0][0]
        cursor.execute(f'''SELECT count(name) FROM students WHERE group_num="C" AND class=(?)''', (clas,))
        groupC = cursor.fetchall()[0][0]
        cursor.execute(f'''SELECT count(name) FROM students WHERE group_num="D" AND class=(?)''', (clas,))
        groupD = cursor.fetchall()[0][0]
        return render_template('class.html', grade = clas, graph_x = x1, graph_y = msy[0], graph_y2 = msy[1], graph_y3 = msy[2], graph_y4 = msy[3], graph_y5 = msy[4], students=students,
                               groupA=groupA,
                               groupB=groupB,
                               groupC=groupC,
                               groupD=groupD
                               )
    else:
        return redirect(f'/', code=302)


    

    
app.register_error_handler(404, handle_not_found)
app.register_error_handler(500, handle_bad_request)
app.run(port=23182, host='0.0.0.0')