CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role INTEGER,
    level INTEGER,
    points INTEGER
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

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions,
    user_id INTEGER REFERENCES users,
    result INTEGER
)

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises,
    user_id INTEGER REFERENCES users,
    rating INTEGER,
    feedback TEXT
)