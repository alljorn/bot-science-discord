import os
import sqlite3


DATA_BASE = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+'/data_base.db')


def initiialize_data_base():
    cursor = DATA_BASE.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guild_config (
            id	            INTEGER NOT NULL UNIQUE,
            director_role	INTEGER DEFAULT NULL,
            writter_role	INTEGER DEFAULT NULL,
            PRIMARY KEY(id)
        );""")
    DATA_BASE.commit()


def reinitiialize_data_base():
    cursor = DATA_BASE.cursor()
    cursor.execute("""DROP TABLE IF EXISTS guild_config;""")
    cursor.execute("""
        CREATE TABLE guild_config (
            id	            INTEGER NOT NULL UNIQUE,
            director_role	INTEGER DEFAULT NULL,
            writter_role	INTEGER DEFAULT NULL,
            PRIMARY KEY(id)
        );""")
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
    reinitiialize_data_base()
else:
    initiialize_data_base()
