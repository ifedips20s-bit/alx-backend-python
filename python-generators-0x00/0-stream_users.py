#!/usr/bin/env python3


from typing import Generator, Dict, Any
import sys


def stream_users() -> Generator[Dict[str, Any], None, None]:
   
    # Import inside function to avoid import-time DB connection during static analysis
    seed = __import__('seed')

    conn = None
    cursor = None
    try:
        conn = seed.connect_to_prodev()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        # Single loop to yield rows one-by-one
        for row in cursor:
            yield row

    finally:
        # Clean up resources
        try:
            if cursor is not None:
                cursor.close()
        except Exception:
            pass
        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass


if __name__ == '__main__':
    for i, user in enumerate(stream_users()):
        print(user)
        if i >= 9:
            break

if __name__ != '__main__':
    sys.modules[__name__] = stream_users