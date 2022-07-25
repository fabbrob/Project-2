import os
import psycopg2
from datetime import datetime

DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping")

class Dashboard:
    def __init__(self, user_id):
        self.current_week = get_current_week()
        self.upcoming_week = self.current_week + 1
        self.correct_tips = get_correct_tips(user_id)
        self.current_week_tips = get_current_week_tips(user_id)

def get_current_week():
    current_time = datetime.now()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT week FROM matches WHERE scheduled <= %s ORDER BY id DESC LIMIT 1', [current_time])
    results = cur.fetchall()
    week_number = results[0][0]
    cur.close()
    conn.close()
    return week_number

def get_correct_tips(user_id):
    week_number = get_current_week()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(matches.id) from matches WHERE matches.week = %s AND matches.winner_id != 0', [week_number])
    results = cur.fetchall()
    season_tips = results[0][0]
    cur.execute('SELECT count(matches.id) from matches INNER JOIN tips ON matches.id = tips.match_id WHERE tips.user_id = %s AND matches.week = %s AND matches.winner_id != 0 AND tips.team_tipped_id = matches.winner_id', [user_id, week_number])
    results = cur.fetchall()
    correct_tips = results[0][0]
    cur.close()
    conn.close()
    return f'{correct_tips}/{season_tips}'

def get_current_week_tips(user_id):
    current_week_tips = []
    week_number = get_current_week()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT teams.abbreviation, teams.logo, tips.team_tipped_id, matches.winner_id FROM matches INNER JOIN tips ON matches.id = tips.match_id INNER JOIN teams ON tips.team_tipped_id = teams.id WHERE tips.user_id = %s AND matches.week = %s ORDER BY matches.scheduled ASC', [user_id, week_number])
    results = cur.fetchall()
    for result in results:
        if result[3] == 0:
            tip_result = 'tg'
        elif result[2] == result[3]:
            tip_result = 'gb'
        else:
            tip_result = 'rb'
        tip = {
            'abbreviation': result[0],
            'logo': result[1],
            'tip_result': tip_result
        }
        current_week_tips.append(tip)
    cur.close()
    conn.close()
    return current_week_tips