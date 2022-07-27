import os
from sqlite3 import connect
from time import time
from unittest import result
import psycopg2
from datetime import datetime, date

DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping")

#DASHBOARD

def get_time_difference_of_timestamps(time1, time2):
    timestamp1 = convert_timestamp_into_timedelta(time1)
    timestamp2 = convert_timestamp_into_timedelta(time2)
    if timestamp1 > timestamp2:
        time_diff = timestamp1 - timestamp2
    else:
        time_diff = timestamp2 - timestamp1
    difference_in_seconds = time_diff.total_seconds()
    return difference_in_seconds


def convert_seconds_to_hours(seconds):
    return seconds % 3600


def convert_timestamp_into_timedelta(timestamp):
    format = '%Y-%m-%d %H:%M:%S'
    return datetime.strptime(timestamp, format)


def get_closest_week():
    time_now = datetime.now()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT scheduled, week
                FROM matches
                WHERE scheduled < %s
                ORDER BY scheduled DESC
                LIMIT 1
                ''', [time_now])
    result = cur.fetchall()
    time_prior = result[0][0]
    week_prior = result[0][1]
    cur.execute('''
                SELECT scheduled, week
                FROM matches
                WHERE scheduled > %s
                ORDER BY scheduled ASC
                LIMIT 1
                ''', [time_now])
    result = cur.fetchall()
    cur.close()
    conn.close()
    time_after = result[0][0]
    week_after = result[0][1]
    if week_prior == week_after:
        return week_prior
    else:
        time_diff_prior = get_time_difference_of_timestamps(time_now, time_prior)
        time_diff_after = get_time_difference_of_timestamps(time_now, time_after)
        if time_diff_prior < time_diff_after:
            return week_prior
        else:
            return week_after


def is_week_complete(week):
    return is_now_after_week(week) and is_week_results_filled(week)


def is_now_after_week(week):
    time_now = datetime.now()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT scheduled
                FROM matches
                WHERE week = %s
                ORDER BY scheduled DESC
                LIMIT 1
                ''', [week])
    result = cur.fetchall()
    cur.close()
    conn.close()
    timestamp = result[0][0]
    time_of_last_game = convert_timestamp_into_timedelta(timestamp)
    return time_of_last_game < time_now


def is_week_results_filled(week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT winner_id
                FROM matches
                WHERE week = %s
                ''', [week])
    results = cur.fetchall()
    cur.close()
    conn.close()
    for result in results:
        if result[0] == 0:
            return False;
    return True
    

def is_week_current(week):
    closest_week = get_closest_week()
    time_now = datetime.now()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT scheduled
                FROM matches
                WHERE week = %s
                ORDER BY scheduled ASC
                LIMIT 1
                ''', [closest_week])
    result = cur.fetchall
    timestamp = result[0][0]
    first_match_timedelta = convert_timestamp_into_timedelta(timestamp)
    cur.execute('''
                SELECT scheduled
                FROM matches
                WHERE week = %s
                ORDER BY scheduled DESC
                LIMIT 1
                ''', [closest_week])
    result = cur.fetchall
    cur.close()
    conn.close()
    timestamp = result[0][0]
    last_match_timedelta = convert_timestamp_into_timedelta(timestamp)
    return time_now > first_match_timedelta and time_now < last_match_timedelta
    

def is_week_upcoming(week):
    return not is_week_complete(week) and not is_week_current(week)


def get_time_until_timestamp(timestamp):
    time_now = datetime.now()
    time_to_compare = convert_timestamp_into_timedelta(timestamp)
    time_diff = get_time_difference_of_timestamps(time_now, time_to_compare)
    hours_until = convert_seconds_to_hours(time_diff)
    if hours_until > 24:
        days_until = hours_until % 24
        return f'{days_until} days'
    elif hours_until == 0:
        return '< 1 hour'
    else:
        return f'{hours_until} hours'


def get_time_until_next_match():
    time_now = datetime.now()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT scheduled
                FROM matches
                WHERE scheduled > %s
                ORDER BY DESC
                LIMIT 1
                ''', [time_now])
    result = cur.fetchall()
    cur.close()
    conn.close()
    time_of_next_match = result[0][0]
    return get_time_until_timestamp(time_of_next_match)


def has_week_been_tipped_by_user(user_id, week):
    if is_week_upcoming(week):
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute('''
                    SELECT COUNT(matches.id)
                    FROM matches
                    INNER JOIN tips ON matches.id = tips.match_id
                    WHERE tips.user_id = %s
                    AND week = %s
                    ''', [user_id, week])
        results = cur.fetchall()
        count_of_tips = results[0][0]
        cur.close()
        conn.close()
        if count_of_tips == 0:
            return False
        else:
            return True
    else:
        return True


def get_users_correct_tips_for_week(user_id, week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT COUNT(tips.id)
                FROM tips
                INNER JOIN matches ON tips.match_id = matches.id
                WHERE tips.user_id = %s
                AND matches.week = %s
                AND tips.team_tipped_id = matches.winner_id
                ''', [user_id, week])
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result[0][0]


def get_total_completed_games_for_week(week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT COUNT(id)
                FROM matches
                WHERE week = %s
                AND winner_id != 0
                ''', [week])
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result[0][0]


def get_total_games_for_week(week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT COUNT(id)
                FROM matches
                WHERE week = %s
                ''', [week])
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result[0][0]


def get_season_tips_for_user(user_id):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT COUNT(tips.id)
                FROM tips
                INNER JOIN matches ON tips.match_id = matches.id
                WHERE tips.user_id = %s
                AND tips.team_tipped_id = matches.winner_id
                ''', [user_id])
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result[0][0]


def get_tips_for_dashboard(user_id, week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT left.id, left.abbreviation, left.logo,
                right.id, right.abbreviation, right.logo,
                tips.team_tipped_id, matches.winner_id
                FROM tips
                FULL JOIN matches on tips.match_id = matches.id
                INNER JOIN teams left on left.id = matches.team1_id
                INNER JOIN teams right on right.id = matches.team2_id
                WHERE matches.week = %s
                AND tips.user_id = %s
                ORDER BY matches.scheduled ASC
                ''', [week, user_id])
    results = cur.fetchall()
    cur.close()
    conn.close()
    return create_tips_for_dashboard(results)


def create_tips_for_dashboard(results):
    tips = []
    for result in results:
        if result[7] == 0: #winner_id
            completed = False
            tip = {
                'left_team_abbreviation': result[1],
                'right_team_abbreviation': result[4],
                'completed': completed
            }
        else:
            completed = True
        
        if completed:
            if result[7] == result[6]: #winner_id == team_tipped_id
                tip_correct = True
            else:
                tip_correct = False
        
        if result[0] == result[6]: #left(team).id = team_tipped_id
            tip = {
                'abbreviation': result[1],
                'logo': result[2],
                'tip_correct': tip_correct,
                'completed': completed
            }
        else:
            tip = {
                'abbreviation': result[4],
                'logo': result[5],
                'tip_correct': tip_correct,
                'completed': completed
            }
        tips.append(tip)
    return tips


def get_tips_for_tips(user_id, week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT left.id, left.abbreviation, left.logo,
                right.id, right.abbreviation, right.logo,
                tips.team_tipped_id, matches.id,
                matches.winner_id, matches_scheduled
                FROM tips
                FULL JOIN matches ON tips.match_id = matches.id
                INNER JOIN teams left ON left.id = matches.team1_id
                INNER JOIN teams right ON right.id = matches.team2_id
                WHERE matches.week = %s
                AND tips.user_id = %s
                ORDER BY matches.scheduled ASC
                ''', [week, user_id])
    results = cur.fetchall()
    cur.close()
    conn.close()
    return create_tips_for_tips(results)


def create_tips_for_tips(results):
    tips = []
    for result in results:
        if result[8] == 0: #winner_id
            completed = False
            tip = {
                'left_id': result[0],
                'left_abbreviation': result[1],
                'left_logo': result[2],
                'right_id': result[3],
                'right_abbreviation': result[4],
                'right_logo': result[5],
                'date': get_date_from_timestamp(result[9]),
                'time': get_time_from_timestamp(result[9]),
                'match_id': result[7],
                'team_tipped_id': result[6],
                'completed': completed
            }
        else:
            completed = True

        if completed:
            if result[8] == result[6]: #winner_id == team_tipped_id
                tip_correct = True
            else:
                tip_correct = False
        
        if result[0] == result[6]: #left.id == team_tipped_id
            tip = {
                'left_id': result[0],
                'left_abbreviation': result[1],
                'left_logo': result[2],
                'right_id': result[3],
                'right_abbreviation': result[4],
                'right_logo': result[5],
                'date': get_date_from_timestamp(result[9]),
                'time': get_time_from_timestamp(result[9]),
                'team_picked': 'left',
                'tip_correct': tip_correct,
                'completed': completed
            }
        else:
            tip = {
                'left_id': result[0],
                'left_abbreviation': result[1],
                'left_logo': result[2],
                'right_id': result[3],
                'right_abbreviation': result[4],
                'right_logo': result[5],
                'date': get_date_from_timestamp(result[9]),
                'time': get_time_from_timestamp(result[9]),
                'team_picked': 'right',
                'tip_correct': tip_correct,
                'completed': completed
            }
        tips.append(tip)
    return tips


def convert_num_to_numth(num):
    end_digit = num % 10
    if end_digit == 1:
        return f'{num}st'
    elif end_digit == 2:
        return f'{num}nd'
    elif end_digit == 3:
        return f'{num}rd'
    else:
        return f'{num}th'


def get_date_from_timestamp(timestamp):
    date_and_time = timestamp.split(' ')
    date_hyphened = date_and_time[0]
    date_arr = date_hyphened.split('-')
    year_int = int(date_arr[0])
    month_int = int(date_arr[1])
    day_int = int(date_arr[2])
    weekday_num = date(year_int, month_int, day_int).weekday()
    weekday_arr = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday = weekday_arr[weekday_num]
    month_arr = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month = month_arr[month_int]
    dayth = convert_num_to_numth(day_int)
    return f'{weekday} {dayth} {month} {year_int}'


def get_time_from_timestamp(timestamp):
    date_and_time = timestamp.split(' ')
    time_coloned = date_and_time[1]
    time = time_coloned.split(':')
    hour_int = int(time[0])
    minute_int = int(time[1])
    if hour_int >= 12:
        meridian = 'PM'
        hour_int -= 12
    else:
        meridian = 'AM'
    return f'{hour_int}:{minute_int} {meridian}'


def get_leaderboard_for_leaderboard(week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT users.id, users.username, COUNT(matches.id)
                FROM users
                INNER JOIN tips ON users.id = tips.user_id
                INNER JOIN matches ON tips.match_id = matches.id
                WHERE matches.week <= week
                AND matches.winner_id = tips.team_tipped_id
                GROUP BY users.id
                ORDER BY COUNT(matches.id)
                ''')
    results = cur.fetchall()
    cur.close()
    conn.close()
    return create_leaderboard_for_leaderboard(results)


def create_leaderboard_for_leaderboard(results):
    leaderboard = []
    for result in results:
        user = {
           'id': result[0],
            'username': result[1],
            'tip_score': result[2]
        }
        leaderboard.append(user)
        leaderboard_length = len(leaderboard)
        user_index = leaderboard_length - 1
        if leaderboard_length > 1:
            previous_user_index = leaderboard_length - 2
            if leaderboard[user_index]['tip_score'] == leaderboard[previous_user_index]['tip_score']:
                leaderboard[user_index]['ranking'] = '-'
                current_index = user_index
                while leaderboard[current_index]['ranking']=='-':
                    current_index -= 1
                leaderboard[user_index]['position'] = convert_numth_to_num(leaderboard[current_index]['ranking'])
            else:
                leaderboard[user_index]['ranking'] = convert_num_to_numth(leaderboard_length)
                leaderboard[user_index]['position'] = leaderboard_length
        else:
            leaderboard[user_index]['ranking'] = '1st'
            leaderboard[user_index]['position'] = 1
    return leaderboard


def user_leaderboard_improvement (user_id, initial_week, final_week):
    leaderboard_initial = get_leaderboard_for_leaderboard(initial_week)
    for user in leaderboard_initial:
        if user['id'] == user_id:
            position_initial = user['position']
    
    leaderboard_final = get_leaderboard_for_leaderboard(final_week)
    for user in leaderboard_final:
        if user['id'] == user_id:
            position_final = user['position']
    
    leaderboard_improvement = position_initial - position_final
    if leaderboard_improvement > 0:
        return f'+{leaderboard_improvement}'
    elif leaderboard_improvement < 0:
        return f'-{leaderboard_improvement}'
    else:
        return '='


def convert_numth_to_num(numth):
    length = len(numth)
    number_end = length - 2
    num_str = numth[0:number_end]
    return int(num_str)