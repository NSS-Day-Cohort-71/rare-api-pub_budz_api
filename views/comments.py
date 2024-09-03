import sqlite3
import json
import datetime

def get_all_comments():
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("SELECT * FROM Comments ORDER BY id ASC")
            comments = db_cursor.fetchall()
            comments_list = [dict(row) for row in comments]
        return json.dumps(comments_list)
    except Exception as e:
        print(f"Error retrieving comments: {str(e)}")
        return json.dumps({"error": "Error retrieving comments"})

def delete_comment(comment_id):
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            db_cursor = conn.cursor()
            db_cursor.execute(
                """
                DELETE FROM Comments
                WHERE id = ?
                """,
                (comment_id,)
            )
            conn.commit()
            return db_cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting comment: {str(e)}")
        return False

def create_comment(comment_data):
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(
                """
                INSERT INTO Comments (post_id, author_id, content)
                VALUES (?, ?, ?)
                """,
                (comment_data['post_id'], comment_data['author_id'], comment_data['content'])
            )
            conn.commit()
            new_comment_id = db_cursor.lastrowid
            db_cursor.execute(
                """
                SELECT * FROM Comments WHERE id = ?
                """,
                (new_comment_id,)
            )
            new_comment = db_cursor.fetchone()
        return json.dumps(dict(new_comment))
    except Exception as e:
        print(f"Error creating comment: {str(e)}")
        return json.dumps({"error": "Error creating comment"})

def update_comment(comment_id, comment_data):
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            db_cursor = conn.cursor()
            db_cursor.execute(
                """
                UPDATE Comments
                SET content = ?
                WHERE id = ?
                """,
                (comment_data["content"], comment_id),
            )
            conn.commit()
            return db_cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating comment: {str(e)}")
        return False

def get_comments_by_post(post_id):
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                SELECT c.id, c.content, c.post_id, c.author_id, c.created_on, 
                       u.username as author_name
                FROM Comments c
                JOIN Users u ON c.author_id = u.id
                WHERE c.post_id = ?
                ORDER BY c.created_on DESC
                """,
                (post_id,)
            )

            comments = db_cursor.fetchall()
            comments_list = [dict(row) for row in comments]

        return json.dumps(comments_list)  # Return just the list

    except Exception as e:
        print(f"Error retrieving comments for post {post_id}: {str(e)}")
        return json.dumps({"error": "Error retrieving comments"})