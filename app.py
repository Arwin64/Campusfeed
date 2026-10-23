"""CampusFeed: a deliberately small social feed for a Git demo."""
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from database import fetch_posts, increment_like_count, initialize_database, insert_post


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(
        SECRET_KEY="workshop-only-not-for-production",
        DATABASE=os.path.join(app.instance_path, "campusfeed.sqlite3"),
    )
    if test_config:
        app.config.update(test_config)
    initialize_database(app.config["DATABASE"])

    @app.get("/")
    def index():
        posts = fetch_posts(app.config["DATABASE"])
        return render_template("feed.html", posts=posts)

    @app.post("/posts")
    def create_post():
        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()
        if not author or not content:
            flash("Add your name and a message to publish a post.")
        elif len(author) > 40 or len(content) > 280:
            flash("Keep names under 40 characters and posts under 280 characters.")
        else:
            insert_post(app.config["DATABASE"], author, content)
        return redirect(url_for("index"))

    @app.post("/posts/<int:post_id>/like")
    def like_post(post_id):
        increment_like_count(app.config["DATABASE"], post_id)
        return redirect(url_for("index"))

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=False)
