import os
from contextlib import asynccontextmanager
from redis_resource import get_redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from domains.base import Base
from domains.raw_matches import RawMatch

DB_HOST = os.environ['POSTGRES_HOST']
DB_NAME = os.environ['POSTGRES_DATABASE']
DB_USER = os.environ['POSTGRES_USER']
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']

class DatabaseManager:
    """Handles all database-related operations."""
    def __init__(self, user, password, host, dbname):
        self.engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}/{dbname}")
        self.Session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def initialize(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(lambda ctx: Base.metadata.create_all(ctx, checkfirst=True))
            await conn.commit()

    @asynccontextmanager
    async def async_session_scope(self):
        async with self.Session() as session:
            try:
                yield session
                await session.commit()
            except:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def insert_file_data(self, match_id):
        match_data = get_redis(match_id)

        if match_data is None:
            print(f"Failed to read match data from {match_id}")
            return

        print(f"Processing match {match_id}")
        try:
            async with self.async_session_scope() as session:
                session.add(RawMatch(
                    match_id=int(match_id),
                    match_data=match_data['info'],
                    deliveries=match_data['innings']
                ))
                await session.flush() 
                print(f"Match with ID {match_id} inserted successfully.")
        except IntegrityError:
            print(f"Match with ID {match_id} already exists in the database.")
            return
        except Exception as e:
            print(f"Error inserting match {match_id}: {e}")
            return

async def insert_match(match_id):
    db_manager = DatabaseManager(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
    await db_manager.initialize()
    await db_manager.insert_file_data(match_id)