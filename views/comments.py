import sqlite3
import json  # Add this line

def get_all_comments():
    """Retrieve all comments from the database."""
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
    """Delete a comment from the database."""
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
            return db_cursor.rowcount > 0  # Return True if comment gets deleted
    except Exception as e:
        print(f"Error deleting comment: {str(e)}")
        return False