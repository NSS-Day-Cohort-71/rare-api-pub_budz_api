import sqlite3
import json


def get_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            Posts.id,
            Posts.title,
            Posts.publication_date,
            Users.first_name || ' ' || Users.last_name AS author,
            Categories.label AS category
        FROM Posts
        JOIN Users ON Posts.user_id = Users.id
        JOIN Categories ON Posts.category_id = Categories.id
        WHERE Posts.approved = 1
        AND Posts.publication_date <= date('now')
        ORDER BY Posts.publication_date DESC
        """
        )

        posts = db_cursor.fetchall()
        posts_list = [dict(row) for row in posts]

    return json.dumps(posts_list)
