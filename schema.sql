
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN
);

DROP TABLE IF EXISTS teams;

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    abbreviation TEXT NOT NULL,
    logo TEXT NOT NULL
);

DROP TABLE IF EXISTS matches;

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    team1_id INTEGER NOT NULL, FOREIGN KEY(team1_id) REFERENCES teams(id),
    team2_id INTEGER NOT NULL, FOREIGN KEY(team2_id) REFERENCES teams(id),
    winner_id INTEGER, FOREIGN KEY(winner_id) REFERENCES teams(id),
    scheduled DATETIME
);

DROP TABLE IF EXISTS tips;

CREATE TABLE tips (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id),
    match_id INTEGER NOT NULL, FOREIGN KEY(match_id) REFERENCES matches(id),
    team_tipped_id INTEGER, FOREIGN KEY(team_tipped_id) REFERENCES teams(id)
);