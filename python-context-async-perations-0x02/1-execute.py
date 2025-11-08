#!/usr/bin/env python3
"""
Reusable context manager for executing SQL queries with parameters.
"""

import sqlite3


class ExecuteQuery:
    """Context manager that opens a DB connection, executes a query,
    and returns the result.
    """

    def __init__(self, db_path, query, params=None):
        self.db_path = db_path
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        """Open connection, execute query, and return results."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        """Commit (if needed) and close connection."""
        if self.conn:
            self.conn.close()
        return False  # Propagate exceptions if any
        

if __name__ == "__main__":
    db_file = "users.db"

    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery(db_file, query, param) as results:
        for row in results:
            print(row)
