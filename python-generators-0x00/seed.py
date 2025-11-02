import mysql.connector
import csv
import uuid
from mysql.connector import errorcode

CSV_PATH = 'user_data.csv'

def connect_db():
    connection = mysql.connector.connect(
        host='localhost',
        port='3306',
        password='i12cuAOL.',
        user='root'
    )
    return connection

def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev DEFAULT CHARACTER SET 'utf8mb4'")
        connection.commit()
    finally:
        cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database (create it first if needed)."""
    conn = mysql.connector.connect(
        host='localhost',
        port='3306',
        password='i12cuAOL.',
        user='root',
        database='ALX_prodev'
    )
    return conn

def create_table(connection):
    """Create user_data table if it does not exist."""
    create_table_sql = (
        "CREATE TABLE IF NOT EXISTS user_data ("
        "user_id CHAR(36) NOT NULL PRIMARY KEY, "
        "name VARCHAR(255) NOT NULL, "
        "email VARCHAR(255) NOT NULL UNIQUE, "
        "age DECIMAL(5,0) NOT NULL"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
    )
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_sql)
        connection.commit()
    finally:
        cursor.close()

def insert_data(connection, data):
    """Insert data into the database.

    Behaviors:
    - If `data` is a dict with keys 'name','email','age', insert a single record and
      return True if inserted, False if skipped because the email already exists.
    - If `data` is a string, treat it as a CSV filepath and seed the DB by calling
      `load_csv_and_seed(connection, data)`; returns the (inserted, skipped) tuple.
    """
    # If caller passed a CSV filename (as in 0-main.py), delegate to load_csv_and_seed
    if isinstance(data, str):
        return load_csv_and_seed(connection, data)

    # Otherwise expect a mapping/dict for a single row insert
    cursor = connection.cursor()
    try:
        # check existence by email
        cursor.execute("SELECT 1 FROM user_data WHERE email = %s", (data['email'],))
        if cursor.fetchone():
            return False

        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
            (user_id, data['name'], data['email'], data['age'])
        )
        connection.commit()
        return True
    finally:
        cursor.close()

def stream_user_data(connection):
    """Generator that yields rows from user_data one by one as dictionaries.

    Usage: for row in stream_user_data(conn): ...
    """
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        for row in cursor:
            yield row
    finally:
        cursor.close()

def load_csv_and_seed(connection, csv_path=CSV_PATH):
    """Read CSV and insert rows into the DB. Returns counts (inserted, skipped)."""
    inserted = 0
    skipped = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            # CSV contains name,email,age
            row = {'name': r['name'].strip('"'), 'email': r['email'].strip('"'), 'age': r['age'].strip('"')}
            try:
                ok = insert_data(connection, row)
                if ok:
                    inserted += 1
                else:
                    skipped += 1
            except mysql.connector.Error as e:
                # If table doesn't exist or other error, raise so caller can handle
                raise
    return inserted, skipped


if __name__ == '__main__':
    # Quick workflow: connect, create DB/table, seed from CSV, then stream back a few rows
    try:
        conn = connect_db()
        create_database(conn)
        conn.close()

        conn = connect_to_prodev()
        create_tabl