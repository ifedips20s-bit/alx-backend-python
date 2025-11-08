#!/usr/bin/env python3
"""
Concurrent asynchronous database queries using aiosqlite and asyncio.gather.
"""

import asyncio
import aiosqlite


async def async_fetch_users(db_path):
    """Fetch all users asynchronously."""
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM users;")
        results = await cursor.fetchall()
        return results


async def async_fetch_older_users(db_path):
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40;")
        results = await cursor.fetchall()
        return results


async def fetch_concurrently(db_path="users.db"):
    """Run both queries concurrently using asyncio.gather."""
    all_users, older_users = await asyncio.gather(
        async_fetch_users(db_path),
        async_fetch_older_users(db_path)
    )

    print("All users:")
    for row in all_users:
        print(row)

    print("\nUsers older than 40:")
    for row in older_users:
        print(row)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
