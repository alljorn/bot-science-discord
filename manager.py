import os, shutil
import time
import sqlite3 as sql


DATA_BASE = sql.connect(os.path.dirname(os.path.abspath(__file__))+'/database.db')


class ArticleDatabase:

    def __init__(self):
        self.con = DATA_BASE
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS " \
                         "article(title, author, timestamp, guild)")
        self.con.commit()

    def get_recent_articles(self):
        res = self.cur.execute("SELECT * FROM article ORDER BY timestamp DESC")
        return res.fetchall()[:10]

    def register_article(self, title, author, guild):
        timestamp = int(time.time())
        self.cur.execute("INSERT INTO article " \
                         f"VALUES (\"{title}\", {author}, {timestamp}, {guild})")
        self.con.commit()


def initialize_data_base():
    try: os.mkdir('articles')
    except FileExistsError:  pass
    cursor = DATA_BASE.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guild_config (
            id	            INTEGER NOT NULL UNIQUE,
            director_role	INTEGER DEFAULT NULL,
            writter_role	INTEGER DEFAULT NULL,
            PRIMARY KEY(id)
        );""")
    DATA_BASE.commit()


def reinitialize_data_base():
    shutil.rmtree('articles')
    cursor = DATA_BASE.cursor()
    cursor.execute("""DROP TABLE IF EXISTS guild_config;""")
    DATA_BASE.commit()
    initialize_data_base()


def is_guild_exists(guild_id: int):
    return get_guild_data(guild_id) is not None


def get_guild_data(guild_id: int):
    cursor = DATA_BASE.cursor()
    response = cursor.execute(f"""SELECT * FROM guild_config WHERE id={guild_id}""")
    guild_data = response.fetchone()
    return guild_data

def add_guild(guild_id: int):
    cursor = DATA_BASE.cursor()
    cursor.execute(f"""
        INSERT INTO guild_config(id)
        VALUES ({guild_id});""")
    DATA_BASE.commit()

def set_director_role(guild_id: int, role_id: int):
    cursor = DATA_BASE.cursor()
    cursor.execute(f"""
        UPDATE guild_config
        SET director_role={role_id}
        WHERE id={guild_id}""")
    DATA_BASE.commit()

def set_writter_role(guild_id: int, role_id: int):
    cursor = DATA_BASE.cursor()
    cursor.execute(f"""
        UPDATE guild_config
        SET writter_role={role_id}
        WHERE id={guild_id}""")
    DATA_BASE.commit()

def get_director_role(guild_id: int):
    data = get_guild_data(guild_id)
    if data is None:
        raise Exception("guild doesn't exist")
    return data[1]

def get_writter_role(guild_id: int):
    data = get_guild_data(guild_id)
    if data is None:
        raise Exception("guild doesn't exist")
    return data[2]


if __name__ == "__main__":
    reinitialize_data_base()
else:
    initialize_data_base()
