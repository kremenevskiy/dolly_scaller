import asyncpg

from src import config


class DatabaseManager:
    pool: asyncpg.Pool | None = None

    @classmethod
    async def init_pool(cls) -> None:
        cls.pool = await asyncpg.create_pool(
            host=config.DatabaseConf.host,
            database=config.DatabaseConf.db_name,
            user=config.DatabaseConf.db_user,
            password=config.DatabaseConf.db_password,
            port=config.DatabaseConf.db_port,
            ssl=None,  # Adjust SSL settings if needed
            min_size=1,  # Minimum number of connections
            max_size=2,  # Maximum number of connections
        )

    @classmethod
    async def close_pool(cls) -> None:
        if cls.pool:
            await cls.pool.close()

    @classmethod
    async def execute(cls, query: str, *args):
        """
        Execute a query without returning results (e.g., INSERT, UPDATE).
        """
        if not cls.pool:
            raise RuntimeError("Database pool is not initialized.")
        async with cls.pool.acquire() as connection:
            await connection.execute(query, *args)

    @classmethod
    async def fetchval(cls, query: str, *args):
        """
        Fetch a single value (e.g., SELECT column FROM ...).
        """
        if not cls.pool:
            raise RuntimeError("Database pool is not initialized.")
        async with cls.pool.acquire() as connection:
            return await connection.fetchval(query, *args)

    @classmethod
    async def fetchrow(cls, query: str, *args):
        """
        Fetch a single row.
        """
        if not cls.pool:
            raise RuntimeError("Database pool is not initialized.")
        async with cls.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    @classmethod
    async def fetch(cls, query: str, *args):
        """
        Fetch multiple rows.
        """
        if not cls.pool:
            raise RuntimeError("Database pool is not initialized.")
        async with cls.pool.acquire() as connection:
            return await connection.fetch(query, *args)
