CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role TEXT
);

CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    question TEXT,
    visible BOOLEAN DEFAULT TRUE,
    day INTEGER
);

CREATE TABLE visible_days (
    id SERIAL PRIMARY KEY,
    day INTEGER,
    visible BOOLEAN DEFAULT FALSE
);

CREATE TABLE assigned_participants (
    id SERIAL PRIMARY KEY,
    participant_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    counselor_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE diary (
    diary_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    date DATE NOT NULL,
    question_id INTEGER REFERENCES questions(question_id) ON DELETE CASCADE,
    answer TEXT,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE follow_up (
    follow_up_id SERIAL PRIMARY KEY,
    counselor_id INTEGER REFERENCES users(id),
    participant_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    question_id INTEGER REFERENCES questions(question_id) ON DELETE CASCADE,
    answer TEXT,
    visible BOOLEAN DEFAULT TRUE
);