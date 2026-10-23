import os
import tempfile
import unittest
from app import create_app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.app = create_app({
            "TESTING": True,
            "DATABASE": os.path.join(self.tempdir.name, "web.sqlite3"),
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.tempdir.cleanup()

    def test_home_renders_posts(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"campusfeed", response.data)
        self.assertIn(b"robotics team", response.data)

    def test_can_create_post(self):
        self.client.post("/posts", data={"author": "Sam", "content": "Hello workshop"})
        self.assertIn(b"Hello workshop", self.client.get("/").data)


if __name__ == "__main__":
    unittest.main()
