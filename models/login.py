import bcrypt
import psycopg2
import os

DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping")

def check_login(email, password):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email LIKE %s", [email])
    results = cur.fetchall()

    if len(results) == 1:
        password_hash = results[0][3]
    else:
        return None
    
    cur.close()
    conn.close()

    valid = bcrypt.checkpw(password.encode(), password_hash.encode())

    if valid:
        user = {
            'id': results[0][0],
            'username': results[0][1],
            'email': results[0][2],
            'password_hash': password_hash,
            'is_admin': results[0][4]
        }
        return user
    else:
        return None


def signup_user(username, email, password):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", [username, email, password_hash])
    conn.commit()
    cur.close()
    conn.close()
    return

