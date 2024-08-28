import sqlite3
import json


def get_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("SELECT * FROM Categories ORDER BY label ASC")

        categories = db_cursor.fetchall()
        categories_list = [dict(row) for row in categories]

    return json.dumps(categories_list)

def update_category(category_id, new_data):
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            db_cursor = conn.cursor()
            # Extract the label from new_data and use it as a parameter
            label = new_data["label"]
            db_cursor.execute(
                """
                UPDATE Categories
                SET label = ?
                WHERE id = ?
                """,
                (label, category_id)  # Use extracted label here
            )
            conn.commit()
            return db_cursor.rowcount > 0  # Return True if the update was successful
    except Exception as e:
        print(f"Error updating category: {str(e)}")
        return False