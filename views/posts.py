import sqlite3
import json
import datetime

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
                CASE 
                    WHEN Categories.label IS NULL THEN 'Uncategorized'
                    ELSE Categories.label
                END AS category,
                Posts.content,
                Posts.image_url,
                Posts.approved,
                Posts.is_deleted
            FROM Posts
            JOIN Users ON Posts.user_id = Users.id
            LEFT JOIN Categories ON Posts.category_id = Categories.id
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



def get_single_post(pk):
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

        db_cursor.execute(
            """ 
        SELECT
            p.id,
            p.title,
            p.publication_date,
            p.user_id,
            CASE 
                WHEN c.label IS NULL THEN 'Uncategorized'
                ELSE c.label
            END AS category,
            p.content,
            p.image_url,
            p.approved,
            p.is_deleted
        FROM Posts p
        LEFT JOIN Categories c ON p.category_id = c.id
        WHERE p.id = ?
        AND p.is_deleted = 0
        """,
            (pk,),
        )
        post = db_cursor.fetchone()

        # Convert the result to a dictionary
        if post:
            return json.dumps(dict(post))
        else:
            return json.dumps({"error": "Post not found"})
    except Exception as e:
        print(f"Error fetching post {pk}: {str(e)}")
        return json.dumps({"error": "Error fetching post"})

def update_post(id, post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Check if the category is "Uncategorized"
        if post_data["category"] == "Uncategorized":
            category_id = None  # Set category_id to None if Uncategorized
        else:
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
                category_id,  # Use the fetched category_id or None
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


def create_post(new_post_data):
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            current_datetime = datetime.datetime.now().strftime('%Y-%m-%d')

            db_cursor.execute(
                """
                INSERT INTO Posts (user_id, publication_date, title, image_url, content, category_id, approved, is_deleted) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
                """,
                (
                    new_post_data["user_id"],
                    current_datetime,
                    new_post_data["title"],
                    new_post_data["image_url"],
                    new_post_data["content"],
                    new_post_data["category_id"],
                    1,
                    0,
                ),
            )

            conn.commit()

            new_post_id = db_cursor.lastrowid
            db_cursor.execute("SELECT * FROM Posts WHERE id = ?", (new_post_id,))
            new_post = db_cursor.fetchone()

            return dict(new_post)
        
    except sqlite3.Error as e:
        print(f"Error creating post: {e}")
        return False
