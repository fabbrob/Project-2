import re
from tabnanny import check
from flask import Flask, redirect, render_template, request, session
import os
import psycopg2
import bcrypt
from models.login import check_login, signup_user, update_profile_in_db, update_password_in_db
from models.dashboard import Dashboard

DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping")
SECRET_KEY = os.environ.get("SECRET_KEY", "pretend key for testing only")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    user_id = session.get("user_id")
    if user_id:
        user_username = session.get("user_username")
        dashboard = Dashboard(user_id)
        return render_template('dashboard.html', username=user_username, dashboard=dashboard)
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

@app.route('/settings')
def settings():
    current_username = session.get('user_username')
    current_email = session.get('user_email')
    return render_template('settings.html', username=current_username, email=current_email)

@app.route('/update_profile', methods=["POST"])
def update_profile():
    new_username = request.form.get('username')
    new_email = request.form.get('email')
    user_id = session.get('user_id')
    update_profile_in_db(user_id, new_username, new_email)
    return redirect('/logout')

@app.route('/change_password', methods=["POST"])
def change_password():
    current_password = request.form.get('password')

    if check_login(session.get('user_email'), current_password):
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if new_password == confirm_password:
            update_password_in_db(session.get('user_id'), new_password)
            return redirect('/logout')
        else:
            return render_template('settings.html', password_error=True)
    else:
        return render_template('settings.html', incorrect_password=True)


@app.route('/tips')
def tips():
    return render_template('base.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)