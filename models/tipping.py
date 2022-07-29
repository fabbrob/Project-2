import psycopg2
import os

DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping")

def does_tip_exist(user_id, tip):
    match_id = tip.split(',')[0]
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT COUNT(id)
                FROM tips
                WHERE user_id = %s
                AND match_id = %s
                ''', [user_id, match_id])
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results[0][0] != 0

def update_tip(user_id, tip):
    match_id = tip.split(',')[0]
    team_tipped_id = tip.split(',')[1]
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                UPDATE tips
                SET team_tipped_id = %s
                WHERE user_id = %s
                AND match_id = %s
                ''', [team_tipped_id, user_id, match_id])
    conn.commit()
    cur.close()
    conn.close()

def create_tip(user_id, tip):
    match_id = tip.split(',')[0]
    team_tipped_id = tip.split(',')[1]
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                INSERT INTO tips (user_id, match_id, team_tipped_id)
                VALUES (%s, %s, %s)
                ''', [user_id, match_id, team_tipped_id])
    conn.commit()
    cur.close()
    conn.close()