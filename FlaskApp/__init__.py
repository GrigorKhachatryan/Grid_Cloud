import psycopg2
import requests
import psycopg2.extras
from flask import Flask, render_template, redirect, request, session
import constant
import test

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
conn = psycopg2.connect(host=constant.host, dbname=constant.name, user=constant.user, password=constant.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


@app.route("/",methods=['GET'])
def info():
    return "VM RUN"


@app.route("/job",methods=['GET'])
def hello():
    cur.execute('select photo,id from task where status=%s',(False,))
    tasks = cur.fetchall()
    for i in tasks:
        number = test.numbercar(i['photo'])
        cur.execute('update task set status=%s, result=%s where id=%s',(True,number,i['id']))
    conn.commit()
    return "Ok"


if __name__ == "__main__":
    app.run('13.90.140.78/')
    requests.get('13.90.140.78')
