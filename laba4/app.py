import requests
from flask import Flask, render_template, request, redirect
import psycopg2
import re

app = Flask(__name__)
conn = psycopg2.connect(
    database="service_db",
    user="postgres",
    password="Dasha1904",
    host="localhost",
    port="5432")

cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username') 
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if len(records) == 1:
                return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
            else:
                return render_template ("login_error.html")
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')

@app.route('/registration/', methods=['POST'])
def registration():
    name = request.form.get("name")
    login = request.form.get("login")
    password = request.form.get("password")
    if len(password) == 0 or len(login) == 0 or len(name) == 0 or len(password) == 0:
        return render_template("r_error.html")
    elif re.findall(r'\d', name)!=[]:
        return render_template("r_error.html")
    cursor.execute("INSERT INTO service.users(full_name, login, password) VALUES(%s, %s, %s);", (str(name), str(login), str(password)))
    conn.commit()
    return redirect ("/login/")
@app.route("/registration/", methods=["GET"])
def registration_page():
    return render_template("registration.html")