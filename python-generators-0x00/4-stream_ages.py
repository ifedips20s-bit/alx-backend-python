
#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination


try:
    for page in lazy_paginator(100):
        for user in page:
            print(user)

except BrokenPipeError:
    sys.stderr.close()

Ayobami Lawal
7:53 PM
#!/usr/bin/python3
"""Memory-efficient age aggregation using generators."""

from typing import Generator


def stream_user_ages() -> Generator[float, None, None]:
    """Generator that yields user ages one by one from the database."""
    seed = __import__('seed')
    conn = None
    cursor = None
    try:
        conn = seed.connect_to_prodev()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")
        
        # Single loop to yield ages one by one
        for row in cursor:
            yield float(row['age'])
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


def calculate_average_age() -> float:
    """Calculate average age using the generator without loading all data."""
    total_age = 0
    count = 0
    
    # Single loop to process ages one by one
    for age in stream_user_ages():
        total_age += age
        count += 1
        
    return total_age / count if count > 0 else 0


if __name__ == '__main__':
    avg_age = calculate_average_age()
    print(f"Average age of users: {avg_age:.2f}")