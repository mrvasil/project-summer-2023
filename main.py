from flask import Flask, render_template, request, redirect
import sqlite3
import hashlib
import secretsq
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
        return render_template('students.html', data=names())
    elif user == 'successfully_student':
        return """ты ученик)<br>
    <a href="/"> <button style="margin-top: 10px;" onclick="exit()">Выйти из аккаунта</button></a>
    <script>function exit() {document.cookie = "user=0"} </script>
    """
    else:
        return redirect("/", code=302)


@app.route('/profile')
def profile():
    name = request.args.get('name')
    class1 = request.args.get('class')
    print(name, class1)
    return "Имя: "+name+"<br>Класс: "+class1

@app.route('/check_password', methods=['POST'])
def check_password():   
    password = request.form['password']
    if hashlib.sha1(password.encode()).hexdigest() == secretsq.pass1:
        return secretsq.secret_cookie
    else:
        return 'Неверный пароль'
    



Dict = {'v': 'Входное тестирование', 't1': '1 триместр', 't2': '2 триместр', 't3': '3 триместр','s1': 'Зимняя сессия', 's2': 'Летняя сессия'}

def into_sql(type, year, mark, name):
    pass

@app.route('/newmark')
def newmark():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        name = request.args.get('name')
        clas = request.args.get('class')
        return render_template('newmark.html', name = name, grade = clas)
    else:
        return redirect("/", code=302)

@app.route('/addmark', methods = ['POST', 'GET'])
def addmark():
    user = request.cookies.get('user')
    if user == secretsq.secret_cookie:
        mark = request.form['mark']
        type = Dict[request.form['type']]
        year = request.form['year']
        name = request.args.get('name')
        clas = request.args.get('class')
        into_sql(type, year, mark, name)
        print(name, clas)
        return redirect(f'/profile?name={name}&class={clas}', 302)
    else:
        return redirect("/", code=302)
    


app.run(port=9127, host='0.0.0.0', debug=True)