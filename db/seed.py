from telnetlib import LOGOUT
import psycopg2
import bcrypt
import os

conn = psycopg2.connect("dbname=esport_tipping")
cur = conn.cursor()

cur.execute('TRUNCATE TABLE users, teams, matches, tips')

cur.execute('DROP TABLE IF EXISTS users CASCADE')
cur.execute('''CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN
)''')

cur.execute('DROP TABLE IF EXISTS teams CASCADE')
cur.execute('''CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    abbreviation TEXT NOT NULL,
    logo TEXT NOT NULL
)''')
cur.execute('DROP TABLE IF EXISTS matches CASCADE')
cur.execute('''CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    team1_id INTEGER NOT NULL, FOREIGN KEY(team1_id) REFERENCES teams(id),
    team2_id INTEGER NOT NULL, FOREIGN KEY(team2_id) REFERENCES teams(id),
    winner_id TEXT,
    scheduled TIMESTAMP
)''')

password = 'rob'
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
cur.execute('INSERT INTO users(username, email, password_hash, is_admin) VALUES (%s, %s, %s, %s)', ['fabbrob', 'robfabbro50@gmail.com', password_hash, 't'])

for line in open('team_data.csv'):
    team_data = line.strip().split(',')
    name = team_data[0]
    abbreviation = team_data[1]
    logo = team_data[2]
    cur.execute("INSERT INTO teams (name, abbreviation, logo) VALUES (%s, %s, %s)", [name, abbreviation, logo])

for line in open('match_data.csv'):
    match_data = line.strip().split(',')
    team1_id = match_data[0]
    team2_id = match_data[1]
    winner_id = match_data[2]
    scheduled = match_data[3]
    cur.execute("INSERT INTO matches (team1_id, team2_id, winner_id, scheduled) VALUES (%s, %s, %s, %s)", [team1_id, team2_id, winner_id, scheduled])

conn.commit()
conn.close()