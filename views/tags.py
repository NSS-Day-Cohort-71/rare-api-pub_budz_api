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

def get_tag_by_id(tag_id):
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("SELECT id, label FROM Tags WHERE id = ?", (tag_id,))
    tag = cursor.fetchone()

    conn.close()

    if tag:
        return {"id": tag[0], "label": tag[1]}
    else:
        return None

def update_tag(tag_id, new_label):
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("UPDATE Tags SET label = ? WHERE id = ?", (new_label, tag_id))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()

    return True if rows_affected > 0 else False


def edit_tag_view(tag_id):
    tag = get_tag_by_id(tag_id)
    if not tag:
        return "Tag not found", 404  # Or handle this according to your framework

    # Render your template here with the tag data (assuming you use templates)
    # In a framework-less approach, you might return the HTML directly
    return f"""
        <h1>Edit Tag</h1>
        <form method="POST" action="/tags/edit/{tag['id']}/">
            <label for="label">Label:</label>
            <input type="text" id="label" name="label" value="{tag['label']}" required>
            <button type="submit">Save</button>
            <button type="button" onclick="window.location.href='/tags'">Cancel</button>
        </form>
    """
def handle_edit_tag_submission(tag_id, form_data):
    new_label = form_data.get('label')
    if new_label:
        update_tag(tag_id, new_label)
        # Redirect back to the tag list or show a success message
        return "Tag updated successfully!", 302  # Redirect to tag list
    else:
        return "Label is required", 400  # Handle error
