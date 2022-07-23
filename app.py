import re
from tabnanny import check
from flask import Flask, redirect, render_template, request, session
import os
import psycopg2
import bcrypt
from models.login import check_login, signup_user

DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping")
SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    user_id = session.get("user_id")
    if user_id:
        user_username = session.get("user_username")
        return f'''<h1>Hello, {user_username}</h1>
                    <a href='/logout'>LOG OUT</a>'''
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
        return render_template('login.html', login_error=True)

@app.route('/logout')
def logout():
    session.pop('user_id')
    session.pop('user_username')
    session.pop('user_email')
    session.pop('user_password_hash')
    session.pop('user_is_admin')
    return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password == confirm_password:
        signup_user(username, email, password)
        # CHANGE THIS REDIRECT TO A LOGIN WHEN YOUR USER HAS SOMEWHERE TO GO
        return redirect('/') 
    else:
        return render_template('login.html', signup_error=True)

if __name__ == "__main__":
    app.run(debug=True)