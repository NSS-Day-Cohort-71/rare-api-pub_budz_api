import sqlite3
import json
from datetime import datetime


def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            select id, username
            from Users
            where username = ?
            and password = ?
        """,
            (user["username"], user["password"]),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {"valid": True, "token": user_from_db["id"]}
        else:
            response = {"valid": False}

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """,
            (
                user["first_name"],
                user["last_name"],
                user["username"],
                user["email"],
                user["password"],
                user["bio"],
                datetime.now(),
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"token": id, "valid": True})


def get_all_users():
    try:
        # Connect to your SQLite database
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Execute a query to get all users
            db_cursor.execute("""
                SELECT
                    id,
                    first_name,
                    last_name,
                    email,
                    bio,
                    username,
                    profile_image_url
                FROM Users
            """)

            # Fetch all the rows returned by the query
            users = db_cursor.fetchall()

            # Convert the rows to a list of dictionaries
            users_list = [dict(user) for user in users]

        # Return the list of users as a JSON string
        return json.dumps(users_list)

    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        return json.dumps({"error": "Failed to retrieve users"})


def get_single_user(user_id):
    try:
        # Connect to your SQLite database
        with sqlite3.connect("./db.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Execute a query to get a single user by their ID
            db_cursor.execute("""
                SELECT
                    id,
                    first_name,
                    last_name,
                    email,
                    bio,
                    username,
                    profile_image_url
                FROM Users
                WHERE id = ?
            """, (user_id,))

            # Fetch the single row returned by the query
            user = db_cursor.fetchone()

            # If user exists, return the user as a dictionary
            if user:
                return json.dumps(dict(user))
            else:
                return json.dumps({"error": "User not found"})

    except Exception as e:
        print(f"Error fetching user: {str(e)}")
        return json.dumps({"error": "Failed to retrieve user"})