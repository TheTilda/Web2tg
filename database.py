import sqlite3
from os import path


def get_script_dir():
    abs_path = path.abspath(__file__) # полный путь к файлу скрипта
    return path.dirname(abs_path)

DB_FILE = get_script_dir() + path.sep + 'base.db'
#Коннект к базе
db = sqlite3.connect(DB_FILE,  check_same_thread=False)
sql = db.cursor()
db.commit()

def create_base():
    sql.execute('''CREATE TABLE IF NOT EXISTS users (
        id BIGINT,
        favorite TEXT
    )''')
    sql.execute('''CREATE TABLE IF NOT EXISTS op (
        channel_id BIGINT,
        name TEXT,
        link TEXT,
        state BIGINT
    )
    ''')
    sql.execute('''CREATE TABLE IF NOT EXISTS posts (
        channel_id BIGINT,
        message_id BIGINT,
        state BIGINT
    )''')
    db.commit()


def get_op():
    sql.execute('SELECT * FROM op WHERE state = 1')
    return sql.fetchone()

def add_user(user_id):
    if sql.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES ({user_id}, '')")
        db.commit()

def add_favorite(link, user_id):
    linked = link.replace('https://', '')
    print(linked)
    print(user_id)
    favorite = (sql.execute(f'SELECT favorite FROM users WHERE id = {user_id}').fetchone())[0] + ' '+linked
    print(favorite)
    sql.execute(f"UPDATE users SET favorite = '{favorite}' WHERE id = {user_id}")
    db.commit()

def get_favorite(user_id):
    return (sql.execute(f"SELECT favorite FROM users WHERE id = {user_id}").fetchone())[0].split()



create_base()