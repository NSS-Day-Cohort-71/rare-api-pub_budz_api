import sqlite3

def get_all_tags():
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("SELECT label FROM Tags ORDER BY label ASC")
    tags = cursor.fetchall()

    conn.close()

    # Convert the list of tuples to a list of strings
    return [tag[0] for tag in tags]
