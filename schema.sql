CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role INTEGER,
    level INTEGER
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER REFERENCES users,
    name TEXT,
    level INTEGER,
    visible INTEGER
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises,
    fin TEXT,
    spa TEXT
);