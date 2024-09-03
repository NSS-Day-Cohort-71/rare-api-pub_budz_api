import sqlite3
import json


def get_posts():
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
            SELECT 
                Posts.id,
                Posts.title,
                Posts.publication_date,
                Users.first_name || ' ' || Users.last_name AS author,
                Categories.label AS category,
                Posts.content,
                Posts.image_url,
                Posts.approved,
                Posts.is_deleted
            FROM Posts
            JOIN Users ON Posts.user_id = Users.id
            JOIN Categories ON Posts.category_id = Categories.id
            WHERE Posts.approved = 1
            AND Posts.is_deleted = 0
            AND Posts.publication_date <= date('now')
            ORDER BY Posts.publication_date DESC
            """
            )

            posts = db_cursor.fetchall()
            posts_list = [dict(row) for row in posts]

        return json.dumps(posts_list)
    except Exception as e:
        print(f"Error fetching posts: {str(e)}")
        return json.dumps({"error": "Error fetching posts"})


def get_single_post(post_id):
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT 
                p.id,
                p.title,
                p.content,
                p.publication_date,
                u.first_name || ' ' || u.last_name AS author,
                c.label AS category
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            JOIN Categories c ON p.category_id = c.id
            WHERE p.id = ?
            """, (post_id,))

            post = db_cursor.fetchone()

            # Convert the result to a dictionary
            if post:
                return json.dumps(dict(post))
            else:
                return json.dumps({"error": "Post not found"})
    except Exception as e:
        print(f"Error fetching post {post_id}: {str(e)}")
        return json.dumps({"error": "Error fetching post"})


def update_post(id, post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Fetch category_id based on category label
        db_cursor.execute(
            """
        SELECT id FROM Categories WHERE label = ?
        """,
            (post_data["category"],),
        )
        category_result = db_cursor.fetchone()

        if category_result:
            category_id = category_result[0]  # Access the first element of the tuple
        else:
            return False  # Return False if the category label doesn't exist

        db_cursor.execute(
            """
        UPDATE Posts
            SET
                title = ?,
                content = ?,
                category_id = ?,
                image_url = ?
            WHERE id = ?
            """,
            (
                post_data["title"],
                post_data["content"],
                category_id,  # Use the fetched category_id
                post_data["image_url"],
                id,
            ),
        )

    return True if db_cursor.rowcount > 0 else False


def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """ 
            UPDATE Posts
            Set is_deleted = 1
            WHERE id = ?
            """,
            (id,),
        )
        conn.commit()

        return True if db_cursor.rowcount > 0 else False
