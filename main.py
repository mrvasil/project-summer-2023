from flask import Flask, render_template, request, redirect
import sqlite3
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
    return render_template('index.html')


@app.route('/students')
def students():
    user = request.cookies.get('user')
    print(user)
    return render_template('names.html', data=names())

@app.route('/profile')
def profile():
    name = request.args.get('name')
    class1 = request.args.get('class')
    print(name, class1)
    return "Имя: "+name+"<br>Класс: "+class1

@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.form['password']
    if password == 'admin':
        return 'successfully993736'
    else:
        return 'Неверный пароль'
    


app.run(port=9127, host='0.0.0.0', debug=True)