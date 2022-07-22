from flask import Flask
import os
import psycopg2
import bcrypt

app = Flask(__name__)

# If the DATABASE_URL is set, use that, otherwuse use local db.
DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping") # Put your DB name

@app.route('/')
def index():
  conn = psycopg2.connect(DB_URL)
  cur = conn.cursor()
  cur.execute('SELECT 1', []) # Query to check that the DB connected
  conn.close()
  return 'Hello, world!'

if __name__ == "__main__":
    app.run(debug=True)