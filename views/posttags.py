import sqlite3

def get_tags_by_post_id(post_id):
    """Fetch all tags associated with a specific post."""
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                SELECT t.id, t.label 
                FROM Tags t
                JOIN PostTags pt ON pt.tag_id = t.id
                WHERE pt.post_id = ?
                """, 
                (post_id,)
            )

            tags = db_cursor.fetchall()
            return [dict(row) for row in tags]

    except Exception as e:
        print(f"Error fetching tags for post {post_id}: {str(e)}")
        return None


def add_tags_to_post(post_id, tag_ids):
    """Associate multiple tags with a post."""
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            db_cursor = conn.cursor()

            for tag_id in tag_ids:
                # Check if the tag already exists for this post
                db_cursor.execute(
                    """
                    SELECT * FROM PostTags
                    WHERE post_id = ? AND tag_id = ?
                    """,
                    (post_id, tag_id)
                )
                result = db_cursor.fetchone()

                if not result:
                    # Only insert if the tag is not already associated with the post
                    db_cursor.execute(
                        """
                        INSERT INTO PostTags (post_id, tag_id)
                        VALUES (?, ?)
                        """, 
                        (post_id, tag_id)
                    )

            conn.commit()
            return True

    except sqlite3.IntegrityError as e:
        print(f"Integrity error associating tags with post {post_id}: {str(e)}")
        return False
    except Exception as e:
        print(f"Error associating tags with post {post_id}: {str(e)}")
        return False


def remove_tags_from_post(post_id, tag_ids=None):
    """Remove all tags associated with a post, or specific tags if provided."""
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            db_cursor = conn.cursor()

            if tag_ids:
                for tag_id in tag_ids:
                    db_cursor.execute(
                        """
                        DELETE FROM PostTags
                        WHERE post_id = ? AND tag_id = ?
                        """, 
                        (post_id, tag_id)
                    )
            else:
                # If no tag_ids are provided, remove all tags for the post
                db_cursor.execute(
                    """
                    DELETE FROM PostTags
                    WHERE post_id = ?
                    """, 
                    (post_id,)
                )

            conn.commit()
            return True

    except Exception as e:
        print(f"Error removing tags from post {post_id}: {str(e)}")
        return False


def get_all_post_tags():
    """Fetch all post-tag associations."""
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                SELECT pt.id, pt.post_id, pt.tag_id, t.label as tag_label
                FROM PostTags pt
                JOIN Tags t ON pt.tag_id = t.id
                ORDER BY pt.post_id ASC
                """
            )

            post_tags = db_cursor.fetchall()
            return [dict(row) for row in post_tags]

    except Exception as e:
        print(f"Error fetching post-tags associations: {str(e)}")
        return None

def delete_post_tag(tag_id):
    """Delete a specific tag association from a post."""
    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            db_cursor = conn.cursor()

            # Delete the post-tag association by its ID
            db_cursor.execute(
                """
                DELETE FROM PostTags
                WHERE id = ?
                """,
                (tag_id,)
            )

            conn.commit()

            # Return True if a row was deleted
            return db_cursor.rowcount > 0

    except Exception as e:
        print(f"Error deleting post-tag association with id {tag_id}: {str(e)}")
        return False