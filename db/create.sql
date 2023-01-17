PRAGMA foreign_keys = on;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (32),
    category_id INTEGER DEFAULT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (32),
    category_id INTEGER NOT NULL,
    type VARCHAR (32),
    address VARCHAR (64) DEFAULT NULL,
    platform VARCHAR (64) DEFAULT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    username VARCHAR (32),
    type VARCHAR (32)
);

DROP TABLE IF EXISTS course_user;
CREATE TABLE course_user (
    course_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

COMMIT TRANSACTION;