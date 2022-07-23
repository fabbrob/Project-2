import re
from tabnanny import check
from flask import Flask, redirect, render_template, request, session
import os
import psycopg2
import bcrypt
from models.login import check_login

DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping")
SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    user_id = session.get("user_id")
    if user_id:
        return 'Hello, world'
    else:
        return redirect('/login')

@app.route('/login')
def login():
    user_id = session.get("user_id")
    if user_id:
        return redirect('/')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    user_object = check_login(email, password)
    if user_object:
        session['user_id'] = user_object['id']
        session['user_username'] = user_object['username']
        session['user_email'] = user_object['email']
        session['user_password_hash'] = user_object['password_hash']
        session['user_is_admin'] = user_object['is_admin']
        return redirect('/')
    else:
        return render_template('login.html', error=True)

@app.route('/signup', methods=['POST'])
def signup():
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)