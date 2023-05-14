import time
import sqlite3 as sql


class ArticleDatabase:

    def __init__(self):
        self.con = sql.connect("data_base.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS " \
                         "article(title, author, timestamp)")

    def get_recent_articles(self):
        res = self.cur.execute("SELECT * FROM article ORDER BY timestamp DESC")
        return res.fetchall()[:20]

    def register_article(self, title, author):
        self.cur.execute("INSERT INTO article " \
                         f"VALUES (\"{title}\", {author}, {int(time.time())})")
        self.con.commit()
