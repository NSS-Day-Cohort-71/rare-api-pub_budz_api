import sqlite3

def get_all_tags():
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    # Select both id and label from the Tags table
    cursor.execute("SELECT id, label FROM Tags ORDER BY label ASC")
    tags = cursor.fetchall()

    conn.close()

    # Convert the list of tuples to a list of dictionaries with id and label
    return [{"id": tag[0], "label": tag[1]} for tag in tags]
