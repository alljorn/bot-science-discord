import os
import sqlite3



DATA_BASE = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+'/data_base.db')


def reinitiialize_data_base():
    cursor = DATA_BASE.cursor()

    cursor.execute("""DROP TABLE IF EXISTS guild_config;""")
    cursor.execute("""
        CREATE TABLE guild_config (
            id	            INTEGER NOT NULL UNIQUE,
            director_role	TEXT DEFAULT NULL,
            writter_role	TEXT DEFAULT NULL,
            PRIMARY KEY(id)
        );""")



def is_guild_exists(guild_id: int):
    return get_guild_data(guild_id) is not None


def get_guild_data(guild_id: int):
    cursor = DATA_BASE.cursor()

    response = cursor.execute(f"""SELECT * FROM guild_config WHERE id={guild_id}""")
    guild_data = response.fetchone()

    return guild_data

def add_guild(guid_id: int):
    cursor = DATA_BASE
    cursor.execute(f"""
        INSERT INTO guild_config(id)
        VALUES ({guid_id});""")
    DATA_BASE.commit()


if __name__=="__main__":
    reinitiialize_data_base()