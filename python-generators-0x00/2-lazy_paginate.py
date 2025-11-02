from typing import Generator, List, Dict, Any

# Helper function to fetch a page of users from the DB

def paginate_users(page_size: int, offset: int) -> List[Dict[str, Any]]:
    seed = __import__('seed')
    conn = None
    cursor = None
    try:
        conn = seed.connect_to_prodev()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        rows = cursor.fetchall()
        return rows
    finally:
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

# Generator for lazy paginated loading

def lazy_paginate(page_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

if __name__ == '__main__':
    # Example: print first 3 pages of users, 4 per page
    for i, page in enumerate(lazy_paginate(4)):
        print(f"Page {i+1}:")
        for user in page:
            print(user)
        print()
        if i >= 2:
            break