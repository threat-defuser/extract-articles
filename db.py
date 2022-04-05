import sqlite3
import time
from contextlib import closing


def make_sure_table_exists(db_file_name: str):
    with closing(sqlite3.connect(db_file_name)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS
                     articles(
                       timestamp INTEGER,
                       site_name TEXT,
                       url TEXT,
                       title TEXT,
                       text TEXT,
                       html TEXT
                       )
                """
            )


def save_entry(
    db_file_name: str, site_name: str, url: str, title: str, text: str, html: str
):
    with closing(sqlite3.connect(db_file_name)) as connection:
        with closing(connection.cursor()) as cursor:
            unix_time = int(time.time())
            cursor.execute(
                "INSERT INTO articles VALUES (?, ?, ?, ?, ?, ?)",
                (unix_time, site_name, url, title, text, html),
            )


def read_entries(db_file_name: str):
    with closing(sqlite3.connect(db_file_name)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM articles").fetchall()
            return rows
