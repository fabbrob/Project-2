import os
from typing import final
import psycopg2
from datetime import datetime, date
import math

DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping")

class Tips:
    def __init__(self, user_id, week):
        self.current_week = week
        #booleans
        self.is_week_completed = is_week_results_filled(week)
        #getters
        self.correct_tips = get_users_correct_tips_for_week(user_id, self.current_week)
        self.completed_games = get_total_completed_games_for_week(self.current_week)
        self.season_tips = get_season_tips_for_user(user_id)
        self.weeks = get_list_of_weeks()
        self.matches = get_matches_for_tips(user_id, self.current_week)

class Dashboard:
    def __init__(self, user_id):
        self.closest_week = get_closest_week()
        self.last_completed_week = get_last_completed_week()
        #booleans
        self.complete = is_week_complete(self.closest_week)
        self.current = is_week_current(self.closest_week)
        self.upcoming = is_week_upcoming(self.closest_week)
        self.tips_entered = has_week_been_tipped_by_user(user_id, self.closest_week)

        #getters
        self.current_correct_tips = get_users_correct_tips_for_week(user_id, self.closest_week)
        self.current_completed_games = get_total_completed_games_for_week(self.closest_week)
        self.completed_correct_tips = get_users_correct_tips_for_week(user_id, self.last_completed_week)
        self.completed_completed_games = get_total_completed_games_for_week(self.last_completed_week)
        self.season_tips = get_season_tips_for_user(user_id)
        self.current_tips = get_tips_for_dashboard(user_id, self.closest_week)
        self.completed_tips = get_tips_for_dashboard(user_id, self.last_completed_week)
        self.matches = get_matches_for_dashboard(self.closest_week)
        self.ranking = get_user_ranking_for_week(user_id, self.closest_week)
        self.improvement = get_user_leaderboard_improvement(user_id, self.last_completed_week-1, self.last_completed_week)
        self.time_until_next_week = get_time_until_next_match()

class Leaderboard:
    def __init__(self):
        self.last_completed_week = get_last_completed_week()
        self.leaderboard = get_leaderboard_for_leaderboard(get_leaderboard(self.last_completed_week), self.last_completed_week)


def get_time_difference_of_timestamps(time1, time2):
    if time1 > time2:
        time_diff = time1 - time2
    else:
        time_diff = time2 - time1
    difference_in_seconds = time_diff.total_seconds()
    return difference_in_seconds


def convert_seconds_to_hours(seconds):
    hours = seconds / 3600
    return math.floor(hours)


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
    time_of_last_game = timestamp
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
    time_now = datetime.now()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT scheduled
                FROM matches
                WHERE week = %s
                ORDER BY scheduled ASC
                LIMIT 1
                ''', [week])
    result = cur.fetchall()
    first_match = result[0][0]
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
    last_match = result[0][0]
    return time_now > first_match and time_now < last_match
    

def is_week_upcoming(week):
    return not is_week_complete(week) and not is_week_current(week)

def get_last_completed_week():
    week = get_closest_week()
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
            return week - 1
    return week

def get_time_until_timestamp(time_to_compare):
    time_now = datetime.now()
    time_diff = get_time_difference_of_timestamps(time_now, time_to_compare)
    time_diff = math.floor(time_diff)
    hours_until = convert_seconds_to_hours(time_diff)
    if hours_until > 24:
        days_until = hours_until / 24
        days_until = math.floor(days_until)
        if days_until == 1:
            return f'{days_until} day'
        else:
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
                ORDER BY scheduled ASC
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

def get_matches_for_dashboard(week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT blue.abbreviation, red.abbreviation
                FROM matches
                INNER JOIN teams blue ON blue.id = matches.team1_id
                INNER JOIN teams red ON red.id = matches.team2_id
                WHERE matches.week = %s
                ORDER BY matches.scheduled ASC
                ''', [week])
    results = cur.fetchall()
    cur.close()
    conn.close()
    return create_matches_for_dashboard(results)

def create_matches_for_dashboard(results):
    matches = []
    for result in results:
        match = {
                'left_team_abbreviation': result[0],
                'right_team_abbreviation': result[1],
        }
        matches.append(match)
    return matches

def get_tips_for_dashboard(user_id, week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''SELECT blue.id, blue.abbreviation, blue.logo,
                red.id, red.abbreviation, red.logo,
                tips.team_tipped_id, matches.winner_id, tips.user_id, matches.id
                FROM tips FULL JOIN matches ON tips.match_id = matches.id
                INNER JOIN teams blue ON blue.id = matches.team1_id
                INNER JOIN teams red ON red.id = matches.team2_id
                WHERE matches.week = %s AND tips.user_id = %s
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
            if does_tip_exist(result[8], f'{result[9]},'):
                if result[0] == result[6]:
                    logo = result[2]
                    abbreviation = result[1]
                else:
                    logo = result[5]
                    abbreviation = result[4]
                tip = {
                    'logo': logo,
                    'abbreviation': abbreviation,
                    'completed': completed
                }
            else:
                tip = {
                    'left_team_abbreviation': result[1],
                    'right_team_abbreviation': result[4],
                    'completed': completed
            }
        else:
            completed = True
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


def get_matches_for_tips(user_id, week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT blue.id, blue.abbreviation, blue.logo,
                red.id, red.abbreviation, red.logo,
                matches.id, matches.scheduled, matches.winner_id
                FROM matches
                INNER JOIN teams blue ON blue.id = matches.team1_id
                INNER JOIN teams red ON red.id = matches.team2_id
                WHERE matches.week = %s
                ORDER BY matches.scheduled ASC
                ''', [week])
    results = cur.fetchall()
    cur.close()
    conn.close()
    return create_matches_for_tips(user_id, results)


def create_matches_for_tips(user_id, results):
    matches = []
    for result in results:
        if result[8] == 0: #winner_id
            completed = False
            if has_match_been_tipped_by_user(user_id, result[6]):
                team_tipped_id = get_user_tip_for_match(user_id, result[6])
                left_tipped = team_tipped_id == result[0]
                right_tipped = team_tipped_id == result[3]
                match = {
                'left_id': result[0],
                'left_abbreviation': result[1],
                'left_logo': result[2],
                'left_tipped': left_tipped,
                'right_id': result[3],
                'right_abbreviation': result[4],
                'right_logo': result[5],
                'right_tipped': right_tipped,
                'date': get_date_from_timestamp(result[7]),
                'time': get_time_from_timestamp(result[7]),
                'match_id': result[6],
                'completed': completed
                }
            else:
                match = {
                'left_id': result[0],
                'left_abbreviation': result[1],
                'left_logo': result[2],
                'right_id': result[3],
                'right_abbreviation': result[4],
                'right_logo': result[5],
                'date': get_date_from_timestamp(result[7]),
                'time': get_time_from_timestamp(result[7]),
                'match_id': result[6],
                'completed': completed
        }
        else:
            completed = True
            team_tipped_id = get_user_tip_for_match(user_id, result[6])
            winner_id = get_winner_for_match(result[6])
            tip_correct = team_tipped_id == winner_id
            left_tipped = team_tipped_id == result[0]
            right_tipped = team_tipped_id == result[3]
            match = {
                'left_id': result[0],
                'left_abbreviation': result[1],
                'left_logo': result[2],
                'left_tipped': left_tipped,
                'right_id': result[3],
                'right_abbreviation': result[4],
                'right_logo': result[5],
                'right_tipped': right_tipped,
                'date': get_date_from_timestamp(result[7]),
                'time': get_time_from_timestamp(result[7]),
                'match_id': result[6],
                'completed': completed,
                'tip_correct': tip_correct
            }
        matches.append(match)
    return matches

def get_winner_for_match(match_id):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT winner_id
                FROM matches
                WHERE id = %s
                ''', [match_id])
    results = cur.fetchall()
    return results[0][0]

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
    timestamp = str(timestamp)
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
    month = month_arr[month_int - 1]
    dayth = convert_num_to_numth(day_int)
    return f'{weekday} {dayth} {month} {year_int}'


def get_time_from_timestamp(timestamp):
    timestamp = str(timestamp)
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


def get_leaderboard(week):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT users.id, users.username, COUNT(matches.id)
                FROM users
                INNER JOIN tips ON users.id = tips.user_id
                INNER JOIN matches ON tips.match_id = matches.id
                WHERE matches.week <= %s
                AND matches.winner_id = tips.team_tipped_id
                GROUP BY users.id
                ORDER BY COUNT(matches.id) DESC
                ''', [week])
    results = cur.fetchall()
    cur.close()
    conn.close()
    return create_leaderboard(results)


def create_leaderboard(results):
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


def get_user_leaderboard_improvement(user_id, initial_week, final_week):
    leaderboard_initial = get_leaderboard(initial_week)
    for user in leaderboard_initial:
        if user['id'] == user_id:
            position_initial = user['position']
    
    leaderboard_final = get_leaderboard(final_week)
    for user in leaderboard_final:
        if user['id'] == user_id:
            position_final = user['position']
    
    leaderboard_improvement = position_initial - position_final
    if leaderboard_improvement > 0:
        return leaderboard_improvement
    elif leaderboard_improvement < 0:
        return leaderboard_improvement
    else:
        return 0

def get_leaderboard_for_leaderboard(leaderboard, final_week):
    initial_week = final_week - 1
    for user in leaderboard:
        user_id = user['id']
        user['improvement'] = get_user_leaderboard_improvement(user_id, initial_week, final_week)
    return leaderboard

def get_user_ranking_for_week(user_id, week):
    leaderboard = get_leaderboard(week)
    for user in leaderboard:
        if user['id'] == user_id:
            position = user['position']
            return convert_num_to_numth(position)
    return


def convert_numth_to_num(numth):
    length = len(numth)
    number_end = length - 2
    num_str = numth[0:number_end]
    return int(num_str)


def get_list_of_weeks():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT week FROM matches ORDER BY week ASC')
    results = cur.fetchall()
    cur.close()
    conn.close()
    weeks = []
    for result in results:
        weeks.append(result[0])
    return weeks

def is_match_complete(match_id):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT winner_id
                FROM matches
                WHERE id = %s
                ''', [match_id])
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results[0][0] != 0

def has_match_been_tipped_by_user(user_id, match_id):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT COUNT(matches.id)
                FROM matches
                INNER JOIN tips
                ON tips.match_id = matches.id
                WHERE matches.id = %s
                AND tips.user_id = %s
                ''', [match_id, user_id])
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results[0][0] != 0

def get_user_tip_for_match(user_id, match_id):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('''
                SELECT tips.team_tipped_id
                FROM matches
                INNER JOIN tips
                ON tips.match_id = matches.id
                WHERE matches.id = %s
                AND tips.user_id = %s
                ''', [match_id, user_id])
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results[0][0]

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