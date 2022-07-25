import os
import psycopg2

DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping")

class Tips:
    def __init__(self, user_id, week):
        self.weeks = get_weeks()
        self.week_score = get_correct_tips_for_week(user_id, week)
        self.season_score = get_season_tips(user_id)
        self.matches = []

def get_weeks():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT week FROM matches ORDER BY week ASC')
    results = cur.fetchall()
    weeks = []
    for result in results:
        weeks.append(result[0])
    return weeks

def get_correct_tips_for_week(user_id, week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(matches.id) from matches WHERE matches.week = %s AND matches.winner_id != 0', [week])
    results = cur.fetchall()
    total_tips = results[0][0]
    cur.execute('SELECT count(matches.id) from matches INNER JOIN tips ON matches.id = tips.match_id WHERE tips.user_id = %s AND matches.week = %s AND matches.winner_id != 0 AND tips.team_tipped_id = matches.winner_id', [user_id, week])
    results = cur.fetchall()
    correct_tips = results[0][0]
    cur.close()
    conn.close()
    return f'{correct_tips}/{total_tips}'

def get_season_tips(user_id):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT count(matches.id) from matches INNER JOIN tips ON matches.id = tips.match_id WHERE tips.user_id = %s AND matches.winner_id != 0 AND tips.team_tipped_id = matches.winner_id', [user_id])
    results = cur.fetchall()
    season_tips = results[0][0]
    cur.close()
    conn.close()
    return season_tips

def get_matches_for_a_week(user_id, week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT matches.scheduled, l.id, l.abbreviation, l.logo, r.id, r.abbreviation, r.logo, matches.winner_id, tips.team_tipped_id FROM matches FULL JOIN tips ON matches.id = tips.match_id INNER JOIN teams l ON matches.team1_id = l.id INNER JOIN teams r ON matches.team2_id = r.id WHERE tips.user_id = %s AND matches.week = %s', [user_id, week])
    results = cur.fetchall()
    for result in results():
        timestamp = convert_timestamp(result[0])
        match = {

        }
    return []

def convert_timestamp(timestamp):
    date = timestamp.split(' ')[0]
    time = timestamp.split(' ')[1]
    return 0


# 0: matches scheduled
# 1: team1 id
# 2: team1 abbr
# 3: team1 logo
# 4: team2 id
# 5: team2 abbr
# 6: team2 logo
# 7: winner id
# 8: team tipped