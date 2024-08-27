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
