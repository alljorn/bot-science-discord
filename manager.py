"""Une librairie pour intéragir avec la base de données.
!!! Exécuté ce fichier, réinitilisera la base de données.
"""

import time
import sqlite3 as sql

DATA_BASE = sql.connect("database.db")


def initiialize_data_base():
    cursor = DATA_BASE.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guild_config (
            id	                INTEGER NOT NULL UNIQUE,
            director_role	INTEGER DEFAULT NULL,
            writer_role	        INTEGER DEFAULT NULL,
            PRIMARY KEY(id)
        );""")
    cursor.execute("CREATE TABLE IF NOT EXISTS " \
                         "article(title, author, timestamp, guild)")
    DATA_BASE.commit()


def reinitiialize_data_base():
    cursor = DATA_BASE.cursor()
    """
    cursor.execute("DROP TABLE IF EXISTS guild_config;")
    cursor.execute(""""""
        CREATE TABLE guild_config (
            id	                INTEGER NOT NULL UNIQUE,
            director_role	INTEGER DEFAULT NULL,
            writer_role	INTEGER DEFAULT NULL,
            PRIMARY KEY(id)
        );"""
    cursor.execute("DROP TABLE IF EXISTS article")
    cursor.execute("CREATE TABLE IF NOT EXISTS " \
                   "article(title, author, timestamp, guild)")
    DATA_BASE.commit()


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


def set_writer_role(guild_id: int, role_id: int):
    cursor = DATA_BASE.cursor()
    cursor.execute(f"""
        UPDATE guild_config
        SET writer_role={role_id}
        WHERE id={guild_id}""")
    DATA_BASE.commit()


def get_director_role(guild_id: int) -> tuple:
    cursor = DATA_BASE.cursor()
    cursor.execute(f"SELECT director_role FROM guild_config WHERE id = {guild_id}")
    return cursor.fetchone()[0]


def get_writer_role(guild_id: int) -> tuple:
    cursor = DATA_BASE.cursor()
    cursor.execute(f"SELECT writer_role FROM guild_config WHERE id = {guild_id}")
    return cursor.fetchone()[0]


def get_recent_articles():
    cursor = DATA_BASE.cursor()
    result = cursor.execute("SELECT * FROM article ORDER BY timestamp DESC")
    return result.fetchall()[:10]


def register_article(title, author, guild):
    timestamp = int(time.time())
    cursor = DATA_BASE.cursor()
    cursor.execute("INSERT INTO article " \
                   f"VALUES (\"{title}\", {author}, {timestamp}, {guild})")
    DATA_BASE.commit()


if __name__ == "__main__":
    reinitiialize_data_base()
else:
    initiialize_data_base()
