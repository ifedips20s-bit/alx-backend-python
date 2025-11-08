#!/usr/bin/env python3
"""
Custom class-based context manager for handling SQLite database connections.
"""

import sqlite3


class DatabaseConnection:
    """Context manager for SQLite database connections."""

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        """Open the database connection."""
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
        # Returning False propagates exceptions (default ALX expectation)
        return False


if __name__ == "__main__":
    # Example usage:
    db_file = "users.db"  # Adjust path if needed

    with DatabaseConnection(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users;")
        results = cursor.fetchall()

        for row in results:
            print(row)
