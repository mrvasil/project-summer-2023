from flask import Flask, render_template, request, redirect
import sqlite3
import secretsq
app = Flask(__name__)


def names():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    sp=[]
    qn = ["five", "six", "seven", "eight", "nine", "ten", "eleven"]
    for i in range(5, 12):
        cursor.execute("SELECT name FROM class"+str(i))
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
        return render_template('names.html', data=names())
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
    if password == secretsq.pass1:
        return secretsq.secret_cookie
    elif password == 'student':
        return 'successfully_student'
    else:
        return 'Неверный пароль'
    



app.run(port=9127, host='0.0.0.0', debug=True)