# CampusFeed

A tiny X-style campus social feed for a Git and GitHub workshop.

The starter has two working features: **view posts** and **create posts**.
It intentionally has **no visible Like button or Search form**; those are the
independent feature-branch assignments for the live demo.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000> in your browser. The first launch creates a small
SQLite database in `instance/campusfeed.sqlite3` and adds five sample posts.

## Worktree ports

For the live workshop, keep a shared virtual environment in the parent
`~/git-live-demo/.venv` directory. Use that interpreter from each worktree
and choose different ports:

```bash
# From the main checkout:
PORT=5000 ../.venv/bin/python app.py

# From a sibling campusfeed-likes worktree:
PORT=5001 ../.venv/bin/python app.py

# From a sibling campusfeed-search worktree:
PORT=5002 ../.venv/bin/python app.py
```

Each worktree initializes its own ignored SQLite database. The table contains a
`like_count` column as starter scaffolding; the student feature adds the actual
Like action and interface.

## Tests

```bash
python -m unittest discover -s tests -v
```

This is a **teaching application**, not a production social network: no real
accounts, CSRF protection, moderation, or production secret management.
Do not deploy it as a public service.
