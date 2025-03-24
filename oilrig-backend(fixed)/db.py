# db.py
import asyncpg
from typing import Optional

DB_POOL: Optional[asyncpg.pool.Pool] = None

async def connect_to_db():
    global DB_POOL
    DB_POOL = await asyncpg.create_pool(
        user='postgres',
        password='giang',
        database='oilrigdb_final',
        host='localhost',
        port=6868,  # Your custom port
        min_size=1,
        max_size=5
    )

async def close_db():
    global DB_POOL
    if DB_POOL:
        await DB_POOL.close()

def get_db_pool():
    return DB_POOL
