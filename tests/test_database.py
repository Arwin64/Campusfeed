"""Tests that do not depend on Flask being installed."""
import os
import tempfile
import unittest
from database import connect, fetch_posts, increment_like_count, initialize_database, insert_post


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tempdir.name, "test.sqlite3")
        initialize_database(self.path)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_seed_posts_and_ignore_repeated_initialization(self):
        self.assertEqual(len(fetch_posts(self.path)), 5)
        initialize_database(self.path)
        self.assertEqual(len(fetch_posts(self.path)), 5)

    def test_create_post(self):
        insert_post(self.path, "Demo Student", "Hello CampusFeed")
        self.assertEqual(fetch_posts(self.path)[0]["content"], "Hello CampusFeed")

    def test_schema_has_reserved_like_count(self):
        with connect(self.path) as db:
            cols = [row[1] for row in db.execute("PRAGMA table_info(posts)").fetchall()]
        self.assertIn("like_count", cols)

    def test_increment_like_count(self):
        post_id = fetch_posts(self.path)[0]["id"]
        increment_like_count(self.path, post_id)
        post = next(post for post in fetch_posts(self.path) if post["id"] == post_id)
        self.assertEqual(post["like_count"], 1)


if __name__ == "__main__":
    unittest.main()
