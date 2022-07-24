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
    winner_id INTEGER,
    scheduled TIMESTAMP,
    week INTEGER
)''')

cur.execute('DROP TABLE IF EXISTS tips CASCADE')
cur.execute('''CREATE TABLE tips (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id),
    match_id INTEGER NOT NULL, FOREIGN KEY(match_id) REFERENCES matches(id),
    team_tipped_id INTEGER, FOREIGN KEY(team_tipped_id) REFERENCES teams(id)
)''')

for line in open('users_data.csv'):
    user_data = line.strip().split(',')
    username = user_data[0]
    email = user_data[1]
    password = user_data[2]
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    is_admin = user_data[3]
    cur.execute("INSERT INTO users (username, email, password_hash, is_admin) VALUES (%s, %s, %s, %s)", [username, email, password_hash, is_admin])

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
    week = match_data[4]
    cur.execute("INSERT INTO matches (team1_id, team2_id, winner_id, scheduled, week) VALUES (%s, %s, %s, %s, %s)", [team1_id, team2_id, winner_id, scheduled, week])

for line in open('tips_data.csv'):
    tips_data = line.strip().split(',')
    user_id = tips_data[0]
    match_id = tips_data[1]
    team_tipped_id = tips_data[2]
    cur.execute("INSERT INTO tips (user_id, match_id, team_tipped_id) VALUES (%s, %s, %s)", [user_id, match_id, team_tipped_id])



conn.commit()
conn.close()