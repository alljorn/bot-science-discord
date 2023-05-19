"""Une librairie pour intéragir avec la base de données.

!!! Exécuté ce fichier, réinitilisera la base de données.
"""

import os
import shutil
import sqlite3 as sql
import time

DATABASE = sql.connect("database.db")


def initialize_database():
    try:
        os.mkdir('articles')
    except FileExistsError:
        pass
    cursor = DATABASE.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guild_config (
            id	                INTEGER NOT NULL UNIQUE,
            director_role	INTEGER DEFAULT NULL,
            writer_role	        INTEGER DEFAULT NULL,
            PRIMARY KEY(id)
        );""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS article(
            title,
            author,
            timestamp,
            guild
        );""")
    DATABASE.commit()


def reinitialize_database():
    if os.path.isdir("articles"):
        shutil.rmtree("articles")
    cursor = DATABASE.cursor()
    cursor.execute("""DROP TABLE IF EXISTS guild_config;""")
    cursor.execute("DROP TABLE IF EXISTS article")
    DATABASE.commit()
    initialize_database()


def is_guild_exists(guild_id: int):
    return get_guild_data(guild_id) is not None


def get_guild_data(guild_id: int):
    cursor = DATABASE.cursor()
    response = cursor.execute(f"""SELECT * FROM guild_config WHERE id={guild_id}""")
    return response.fetchone()


def add_guild(guild_id: int):
    cursor = DATABASE.cursor()
    cursor.execute(f"""
        INSERT INTO guild_config(id)
        VALUES ({guild_id});""")
    DATABASE.commit()


def set_director_role(guild_id: int, role_id: int):
    cursor = DATABASE.cursor()
    cursor.execute(f"""
        UPDATE guild_config
        SET director_role={role_id}
        WHERE id={guild_id}""")
    DATABASE.commit()


def set_writer_role(guild_id: int, role_id: int):
    cursor = DATABASE.cursor()
    cursor.execute(f"""
        UPDATE guild_config
        SET writer_role={role_id}
        WHERE id={guild_id}""")
    DATABASE.commit()


def get_director_role(guild_id) -> int:
    cursor = DATABASE.cursor()
    cursor.execute(f"SELECT director_role FROM guild_config WHERE id = {guild_id}")
    return cursor.fetchone()[0]


def get_writer_role(guild_id) -> int:
    cursor = DATABASE.cursor()
    cursor.execute(f"SELECT writer_role FROM guild_config WHERE id = {guild_id}")
    return cursor.fetchone()[0]


def get_recent_articles(guild_id):
    cursor = DATABASE.cursor()
    result = cursor.execute(f"SELECT * FROM article WHERE guild = {guild_id} "  \
                            "ORDER BY timestamp DESC")
    return result.fetchmany(size=10)


def register_article(title, author, guild):
    timestamp = int(time.time())
    cursor = DATABASE.cursor()
    cursor.execute("INSERT INTO article " \
                   f"VALUES (\"{title}\", {author}, {timestamp}, {guild})")
    DATABASE.commit()


if __name__ == "__main__":
    reinitialize_database()
else:
    initialize_database()
