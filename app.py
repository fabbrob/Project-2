import re
from flask import Flask, redirect, render_template, request, session
import os
import psycopg2
import bcrypt

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
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)