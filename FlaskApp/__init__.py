import requests
import time
import base64
import psycopg2
import subprocess
import psycopg2.extras
from requests.exceptions import ConnectionError
from flask import Flask, render_template, redirect, request, session
import constant

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
conn = psycopg2.connect(host=constant.host, dbname=constant.name, user=constant.user, password=constant.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
status = False

@app.route("/")
def hello():
    print(session)
    if session:
        return redirect('/task')
    return render_template('index.html')


@app.route('/reg', methods=['POST'])
def registration():
    email = request.form['email']
    password = request.form['password']

    cur.execute('select * from client where email=%s',(email,))
    user = cur.fetchone()
    if user == None:
        cur.execute('insert into client (email,password) values (%s,%s)',(email,password))
        conn.commit()
        session['email'] = email
        return redirect('/task')
    else:
        if user['password'] == password:
            session['email'] = email
            return redirect('/task')
    return 'not correct email or password'


@app.route('/task')
def task():
    print(session['email'])
    cur.execute('select * from task where status=False')
    count = cur.fetchall()
    if len(count) > 5:
        status = True
        subprocess.Popen('bash /var/www/FlaskApp/FlaskApp/login.sh', shell=True)
        subprocess.Popen('bash /var/www/FlaskApp/FlaskApp/start.sh', shell=True)
        try:
            k = requests.get('http://13.90.140.78/job')
        except ConnectionError as e:
            print(e)
            time.sleep(1)
            return redirect('/task')
    cur.execute('select * from task where status=False')
    count = cur.fetchall()
    if len(count) < 1:
        status = False
        subprocess.Popen('bash /var/www/FlaskApp/FlaskApp/login.sh', shell=True)
        subprocess.Popen('bash /var/www/FlaskApp/FlaskApp/stop.sh', shell=True)
    cur.execute('select count(id) from task where email=%s and status=%s',(session['email'],False))
    tasks = cur.fetchone()
    cur.execute('select id,result from task where email=%s and status=%s',(session['email'],True))
    result = cur.fetchall()
    for i in result:
        i['result'] = i['result'].decode('utf-8')
    tasks = tasks['count']
    return render_template('task.html', task=tasks, result=result)


@app.route('/newtask', methods=['POST'])
def newtask():
    image = request.files['file']
#    image_data = bytes(image, encoding="ascii")
    image_string =bytes(image.stream._file.getvalue())
    image_base64 = base64.b64encode(image_string)
    if len(image_base64) > 10:
        cur.execute('insert into task (photo,status,result,email) values(%s,%s,%s,%s)',(image_base64,False,None,session['email']))
    conn.commit()
    return redirect('/task')

@app.route('/logout')
def logout():
       # remove the username from the session if it is there
       session.pop('email', None)
       return redirect('/')



if __name__ == "__main__":
    app.run()
