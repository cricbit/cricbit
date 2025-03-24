import pandas as pd

from contextlib import asynccontextmanager
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from domains.base import Base
from domains.raw_matches import RawMatch
from domains.raw_players import RawPlayer

class DatabaseService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, user=None, password=None, host=None, dbname=None, port=None):
        if not hasattr(self, 'engine'):
            connection_string = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"
            self.engine = create_async_engine(
                connection_string,
                connect_args={
                    "statement_cache_size": 0,
                    "prepared_statement_cache_size": 0,
                    "server_settings": {
                        "statement_timeout": "0",
                        "idle_in_transaction_session_timeout": "0"
                    }
                },
                pool_pre_ping=True,
                pool_size=20,
                max_overflow=30,
                pool_timeout=60,
                execution_options={"prepare": False}
            )
            self.Session = sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )

    @asynccontextmanager
    async def async_session_scope(self):
        async with self.Session() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    async def initialize(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def insert_match(self, match_id: int, match_data: dict) -> bool:
        if not match_data:
            print(f"Failed to read match data from {match_id}")
            return False

        try:
            async with self.async_session_scope() as session:
                match = RawMatch(
                    match_id=int(match_id),
                    match_data=match_data['info'],
                    deliveries=match_data['innings']
                )
                session.add(match)
                await session.flush()
                print(f"Match with ID {match_id} inserted successfully.")
                return True
        except IntegrityError:
            print(f"Match with ID {match_id} already exists in the database.")
            return False
        except Exception as e:
            print(f"Error inserting match {match_id}: {e}")
            return False

    async def get_total_matches(self) -> int:
        async with self.async_session_scope() as session:
            result = await session.execute(select(func.count()).select_from(RawMatch))
            return result.scalar_one()

    async def get_match_by_id(self, match_id: int) -> RawMatch:
        async with self.async_session_scope() as session:
            result = await session.execute(select(RawMatch).where(RawMatch.match_id == match_id))
            return result.scalar_one_or_none()

    async def add_player(self, player_id: int, player_data: pd.Series) -> bool:
        async with self.async_session_scope() as session:
            try:
                # Check if player already exists
                existing_player = await session.execute(
                    select(RawPlayer).where(RawPlayer.player_id == player_id)
                )
                if existing_player.scalar_one_or_none():
                    return True  # Player exists, skip

                if not pd.isna(player_data.get('key_cricinfo')):
                    player = RawPlayer(
                        player_id=player_id,
                        name=player_data.get('name'),
                        cricinfo_id=player_data.get('key_cricinfo'),
                    )
                    session.add(player)
                    await session.flush()
                    return True
            except Exception as e:
                print(f"Error processing player {player_id}: {e}")
                return False

    async def get_players_count(self) -> int:
        async with self.async_session_scope() as session:
            result = await session.execute(select(func.count()).select_from(RawPlayer))
            return result.scalar_one()