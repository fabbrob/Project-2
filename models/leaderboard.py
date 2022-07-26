from mimetypes import init
import os
import psycopg2
from datetime import datetime

DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping")

class Leaderboard:
    def __init__(self):
        self.leaderboard = get_leaderboard()

    def get_sorted_leaderboard(self):
        sorted_leaderboard = self.leaderboard
        for i in range(1, len(sorted_leaderboard)):
            tipper_to_sort = sorted_leaderboard[i]
            j = i - 1

            while j >= 0 and sorted_leaderboard[j]['total_tips'] <= tipper_to_sort['total_tips']:
                sorted_leaderboard[j+1] = sorted_leaderboard[j]
                j -= 1
        
            sorted_leaderboard[j + 1] = tipper_to_sort
        return sorted_leaderboard

class Leaderboard_Entry:
    def __init__(self, user_id):
        leaderboard = get_leaderboard()
        self.season_tips = get_total_tips(user_id)
        self.position = get_user_position(user_id, leaderboard)
        prev_leaderboard = get_leaderboard_up_to_week(get_previous_week())
        self.improvement = get_improvement(user_id, leaderboard, prev_leaderboard)


def get_leaderboard():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT id, username FROM users')
    users = cur.fetchall()
    leaderboard = []
    for user in users:
        leaderboard.append(make_leaderboard_object(user[0], user[1]))
    for user in leaderboard:
        user['position'] = get_user_position(user['id'], leaderboard)
    prev_leaderboard = get_leaderboard_up_to_week(get_previous_week())
    for user in leaderboard:
        user['improvement'] = get_improvement(user['id'], leaderboard, prev_leaderboard)
    return leaderboard

def get_sorted_leaderboard(self):
        sorted_leaderboard = self.leaderboard
        for i in range(1, len(sorted_leaderboard)):
            tipper_to_sort = sorted_leaderboard[i]
            j = i - 1

            while j >= 0 and sorted_leaderboard[j]['total_tips'] <= tipper_to_sort['total_tips']:
                sorted_leaderboard[j+1] = sorted_leaderboard[j]
                j -= 1
        
            sorted_leaderboard[j + 1] = tipper_to_sort
        return sorted_leaderboard

def get_leaderboard_up_to_week(week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT id, username FROM users')
    users = cur.fetchall()
    leaderboard = []
    for user in users:
        leaderboard.append(make_leaderboard_object_with_week(user[0], user[1], week))
    for user in leaderboard:
        user['position'] = get_user_position(user['id'], leaderboard)
    return leaderboard

def get_total_tips(user_id):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT count(matches.id) from matches INNER JOIN tips ON matches.id = tips.match_id WHERE tips.user_id = %s AND tips.team_tipped_id = matches.winner_id', [user_id])
    results = cur.fetchall()
    total_tips = results[0][0]
    cur.close()
    conn.close()
    return total_tips

def get_total_tips_up_to_week(user_id, week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT count(matches.id) from matches INNER JOIN tips ON matches.id = tips.match_id WHERE tips.user_id = %s AND tips.team_tipped_id = matches.winner_id AND matches.week <= %s', [user_id, week])
    results = cur.fetchall()
    total_tips = results[0][0]
    cur.close()
    conn.close()
    return total_tips

def make_leaderboard_object(user_id, user_username):
    leaderboard_obj = {
        'id': user_id,
        'username': user_username,
        'total_tips': get_total_tips(user_id)
    }
    return leaderboard_obj

def make_leaderboard_object_with_week(user_id, user_username, week):
    leaderboard_obj = {
        'id': user_id,
        'username': user_username,
        'total_tips': get_total_tips_up_to_week(user_id, week)
    }
    return leaderboard_obj

def get_user_position(user_id, leaderboard):
    position = 1
    for user in leaderboard:
        if user['id'] == user_id:
            for user_to_compare in leaderboard:
                if user['total_tips'] < user_to_compare['total_tips']:
                    position += 1
    return convert_num_to_position(position)

def convert_num_to_position(number):
    if number % 10 == 1:
        return f'{number}st'
    elif number % 10 == 2:
        return f'{number}nd'
    elif number % 10 == 3:
        return f'{number}rd'
    else:
        return f'{number}th'

def convert_position_to_num(position):
    disallowed_chars = ['t', 'h', 's', 'n', 'd', 'r']
    for char in disallowed_chars:
        position = position.replace(char, '')
    return int(position)

def get_previous_week():
    previous_time = datetime.now()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT week, winner_id FROM matches WHERE scheduled <= %s ORDER BY id', [previous_time])
    results = cur.fetchall()
    cur.close()
    conn.close()
    for result in results:
        week = result[0]
        winner_id = result[1]
        if winner_id == 0:
            return week - 1
    return week

def get_improvement(user_id, current_leaderboard, previous_leaderboard):
    now_pos = get_user_position(user_id, current_leaderboard)
    prev_pos = get_user_position(user_id, previous_leaderboard)
    now_int = convert_position_to_num(now_pos)
    prev_int = convert_position_to_num(prev_pos)
    improvement_int = prev_int - now_int
    if improvement_int > 0:
        return f'+{improvement_int}'
    elif improvement_int < 0:
        return f'-{improvement_int}'
    else:
        return '-'