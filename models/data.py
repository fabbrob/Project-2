import os
import psycopg2
from datetime import datetime, date

DB_URL = os.environ.get("DATABASE_URL", "dbname=esport_tipping")

class Dashboard:
    def __init__(self, user_id):
        self.current_week = get_current_week()
        self.upcoming_week = self.current_week + 1
        self.correct_tips = get_correct_tips(user_id)
        self.current_week_tips = get_current_week_tips(user_id)

class Leaderboard_Entry:
    def __init__(self, user_id):
        leaderboard = get_leaderboard()
        self.season_tips = get_total_tips(user_id)
        self.position = get_user_position(user_id, leaderboard)
        prev_leaderboard = get_leaderboard_up_to_week(get_previous_week())
        self.improvement = get_improvement(user_id, leaderboard, prev_leaderboard)

class Tips:
    def __init__(self, user_id, week):
        self.weeks = get_weeks()
        self.week_score = get_correct_tips_for_week(user_id, week)
        self.season_score = get_season_tips(user_id)
        self.matches = []

#DASHBOARD

#get closest week number
    #get time of now
    #get time of first match prior to time
    #get time of first match after time
        #if week of both matches match
        #return the week
    #otherwise check which match is closer
    #return week of that match

#is week complete (week)
    #set week as closest week
    #get timestamp of last match of week
    #if last timestamp is before
        #return true
    #else
        #return false

#is closest week current
    #get closest week
    #get timestamp of first match of said week
    #get timestamp of last match of said week
    #if first timestamp is before and last is after
        #return true
    #else
        #return false

#is closest week upcoming
    #return NOT is closest week complete AND NOT is closest week current

#get time before week start
    #get current date
    #get closest week
    #get timestamp of first match
    #compare current date and timestamp and return value
    #(maybe get time in terms of hours and then you can convert it however you want to)

#has upcoming week been tipped
    #IF is closest week upcoming
        #get user_id
        #get closest week
        #get count from tips where user id = user AND week = closest week
        #IF count == 0
            #return false
        #ELSE 
            #return true
    #ELSE
        #return false

#get correct tips for a week (week)
    #connect to db
    #get count FROM tips 
    #JOIN matches ON match_id 
    #WHERE id = user_id AND tips.team_tipped_id = match.winner_id AND matches.week = week
    #get result
    #disconnect
    #return result

#get total played games from a week (week)
    #get current time
    #connect to db
    #get count from matches
    #where week = week and timestamp <= current time (newest time = biggest)
    #get result
    #disconnect
    #return result

#get total games for a week (week)
    #connect to db
    #get count from matches where week = week
    #get result
    #disconnect
    #return result

#get season tips (user_id)
    #connect to db
    #get count from tips
    #join matches on match id
    #where team tipped = winner id and user id = user id
    #get result
    #disconnect
    #return result

#get tips for dashboard (user_id, week)
    #connect to db
    #SELECT
    # left.id, left.abbreviation, left.logo,
    # right.id, right.abbreviation, right.logo,
    # tips.team_tipped_id, matches.winner_id
    #from tips
    #full join matches on matches.id = tips.match_id
    #inner join teams left on left.id = tips.team_team1.id
    #inner join teams right on right.id = matches.team2.id
    #where matches.week = week AND user_id = tips.user_id
    #order by matches.scheduled asc
    #get results
    #set tips = []
    # for result in result
        #if (winner_id) result[7] == 0
            #completed = false
            #tip = {
            #   'left_team_abbreviation': result[1](abbr)
            #   'right_team_abbreviation': result[4](abbr)
            #   'completed': False
            # }
        #else
            #completed = true
        #----
        #if completed
            #if result[7](winner_id) == result[6](team_tipped_id)
                #tip_correct = true
            #else
                #tip_correct = false
        #----
        # if result[0](left.id)==result[6](team_tipped_id)
            #tip = {
            #   'abbreviation' = result[1](left.abbreviation)
            #   'logo' = result[2](left.logo)
            #   'tip_correct' = tip_correct
            #   'completed' = completed
            # }
        # else:
            #tip = {
            #   'abbreviation' = result[4](right.abbreviation)
            #   'logo' = result[5](right.logo)
            #   'tip_correct' = tip_correct
            #   'completed' = completed
            # }
        #tips.append(tip)
    #return tips

#get tips for tips (user_id, week)
    #connect to db
    #SELECT
    # left.id, left.abbreviation, left.logo,
    # right.id, right.abbreviation, right.logo,
    # tips.team_tipped_id, match_id,
    # matches.winner_id, matches.scheduled
    #from tips
    #full join matches on matches.id = tips.match_id
    #inner join teams left on left.id = tips.team_team1.id
    #inner join teams right on right.id = matches.team2.id
    #where matches.week = week AND user_id = tips.user_id
    #order by matches.scheduled asc
    #get results
    #set tips = []
    # for result in result
        #if (winner_id) result[8] == 0
            #completed = false
            #tip = {
            #   'left_team_id': result[0](id)
            #   'left_team_abbreviation': result[1](abbr)
            #   'left_team_logo': result[2](logo)
            #   'right_team_id': result[3](id)
            #   'right_team_abbreviation': result[4](abbr)
            #   'right_team_logo': result[5](logo)
            #   'date': get_date_from_timestamp(result[9]) (timestamp)
            #   'time': get_time_from_timestamp(result[9]) (timestamp)
            #   'match_id': result[7](match_id)
            #   'team_tipped_id': result[6](team_tipped)
            #   'completed': False
            # }
        #else
            #completed = true
        #----
        #if completed
            #if result[8](winner_id) == result[6](team_tipped_id)
                #tip_correct = true
            #else
                #tip_correct = false
        #----
        # if result[0](left.id)==result[6](team_tipped_id)
            #tip = {
            #   'left_team_id': result[0](id)
            #   'left_team_abbreviation': result[1](abbr)
            #   'left_team_logo': result[2](logo)
            #   'right_team_id': result[3](id)
            #   'right_team_abbreviation': result[4](abbr)
            #   'right_team_logo': result[5](logo)
            #   'date': get_date_from_timestamp(result[9]) (timestamp)
            #   'time': get_time_from_timestamp(result[9]) (timestamp)
            #   'team_picked_left': True
            #   'tip_correct' = tip_correct
            #   'completed' = completed
            # }
        # else:
            #tip = {
            #   'left_team_id': result[0](id)
            #   'left_team_abbreviation': result[1](abbr)
            #   'left_team_logo': result[2](logo)
            #   'right_team_id': result[3](id)
            #   'right_team_abbreviation': result[4](abbr)
            #   'right_team_logo': result[5](logo)
            #   'date': get_date_from_timestamp(result[9]) (timestamp)
            #   'time': get_time_from_timestamp(result[9]) (timestamp)
            #   'team_picked_right': True
            #   'tip_correct' = tip_correct
            #   'completed' = completed
            # }
        #tips.append(tip)
    #return tips

#convert_num_to_numth(num)
    #end_digit = num % 10
    #if end_digit == 1:
        #return f'{num}st'
    #elif end_digit == 2:
        #return f'{num}nd'
    #elif end_digit == 3:
        #return f'{num}rd'
    #else
        #return f'{num}th'

#get_date_from_timestamp (timestamp)
    #date_and_time = timestamp.split(' ')
    #date_hyphened = date_and_time[0]
    #date = date_hyphened.split('-')
    #year_int = int(date[0])
    #month_int = int(date[1])
    #day_int = int(date[2])
    #weekday_num = date(year, month, day).weekday()
    #if weekday_num == 0:
        #weekday = 'Monday'
    #....
    #else if weekday_num == 6:
        #weekday = 'Sunday'
    ##
    #if month == 1:
        #month == 'January'
    #...
    #else if month == 12:
        #month == 'December'
    ##
    #dayth = convert_num_to_numth(num)
    #return f'{weekday} {dayth} {month} {year_int}'

#get_time_from_timestamp (timestamp)
    #date_and_time = timestamp.split(' ')
    #time_coloned = date_and_time[1]
    #time = #time_coloned.split(':')
    #hour_int = int(time[0])
    #minute_int = int(time[1])
    #if hour_int >= 12
        #meridian = 'PM'
        #hour_int -= 12
    #else
        #meridian = 'AM'
    #return f'{hour_int}:{minute_int} {meridian}'

#get leaderboard(week)
    #connect to db
    #SELECT users.id, users.username, COUNT(matches.id)
    #FROM users
    #INNER JOIN tips ON users.id = tips.user_id
    #INNER JOIN matches ON tips.match_id = matches.id
    #WHERE matches.week <= week AND matches.winner_id = tips.team_tipped_id
    #GROUP BY users.id
    #ORDER BY COUNT(matches.id) DESC
    #results = cur.fetchall()
    #users = []
    #for result in results
        #user_obj = {
        # 'id': result[0]
        # 'username': result[1]
        # 'tip_score': result[2]
        # }
        #users.append(user_obj)
        #users_length = len(users)
        #user_index = users_length - 1
        #if users_length > 1:
            #previous_user_index = users_length - 2
            #if users[user_index]['tip_score'] == users[previous_user_index]['tip_score']
                #users[user_index]['ranking'] = '-'
                #current_index = user_index
                #while users[current_index]['ranking']=='-'
                    #current_index -= 1
                #users[user_index]['position'] = convert_numth_to_num(users[current_index]['ranking'])
            #else
                #users[user_index]['ranking'] = convert_num_to_numth(users_length)
                #users[user_index]['position'] = users_length
        #else:
            #users[user_index]['ranking'] = '1st'
            #users[user_index]['position'] = 1
    #return users

#get user leaderboard improvement (user_id, initial_week, final_week)
    #leaderboard_initial = get_leaderboard(initial_week)
    #for user in leaderboard_initial:
        #if user['id'] == user_id
            #position_initial = user['position]
    ##
    #leaderboard_final = get_leaderboard(final_week)
    #for user in leaderboard_final:
        #if user['id'] == user_id
            #position_final = user['position]
    ##
    #leaderboard_improvement = position_inital - position_final
    #if leaderboard_improvement > 0:
        #return f'+{leaderboard_improvement}'
    #elif leaderboard_improvement < 0:
        #return f'-{leaderboard_improvement}'
    #else
        #return '='

#convert_numth_to_num(numth)
    #length = len(numth)
    #number_end = length - 2
    #num_str = numth[0:number_end]
    #return int(num_str)


