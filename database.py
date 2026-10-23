"""SQLite helpers for the CampusFeed Git workshop."""
import os
import sqlite3
from contextlib import contextmanager

SEED_POSTS = [
    ("Aarav", "The open-source meetup is starting at 4 PM today. Bring your laptop!"),
    ("Nila", "Anyone interested in a weekend UI design challenge?"),
    ("Kiran", "Our robotics team is looking for Python contributors."),
    ("Maya", "The photography club is hosting a campus photo walk."),
    ("Ishaan", "Sharing some notes from yesterday's database workshop."),
]


@contextmanager
def connect(database_path):
    db = sqlite3.connect(database_path)
    db.row_factory = sqlite3.Row
    try:
        with db:
            yield db
    finally:
        db.close()


def initialize_database(database_path):
    os.makedirs(os.path.dirname(os.path.abspath(database_path)), exist_ok=True)
    with connect(database_path) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                content TEXT NOT NULL,
                like_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        if db.execute("SELECT COUNT(*) FROM posts").fetchone()[0] == 0:
            db.executemany(
                "INSERT INTO posts (author, content) VALUES (?, ?)", SEED_POSTS
            )


def fetch_posts(database_path):
    with connect(database_path) as db:
        return db.execute(
            "SELECT id, author, content, like_count, created_at "
            "FROM posts ORDER BY id DESC"
        ).fetchall()


def insert_post(database_path, author, content):
    with connect(database_path) as db:
        db.execute(
            "INSERT INTO posts (author, content) VALUES (?, ?)",
            (author, content),
        )


def increment_like_count(database_path, post_id):
    with connect(database_path) as db:
        db.execute(
            "UPDATE posts SET like_count = like_count + 1 WHERE id = ?",
            (post_id,),
        )
