import sqlite3
import os
from settings import BASE_DIR, DB_NAME


def create_db():
    con = sqlite3.connect(os.path.join(BASE_DIR, 'db', DB_NAME))
    cur = con.cursor()
    with open('create.sql', 'r') as f:
        text = f.read()
    cur.executescript(text)
    cur.close()
    con.close()


if __name__ == '__main__':
    create_db()
