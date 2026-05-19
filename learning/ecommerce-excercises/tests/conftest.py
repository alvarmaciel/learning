import asyncio
import binascii
import os

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from ecommerce.infrastructure.database import mapper_registry
from ecommerce.infrastructure import entity_mappings  # noqa: F401 — triggers table registration


# Reads from env — works both locally (db on localhost) and inside Docker (db on "db" host)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "root")
DB_PORT = os.getenv("DB_PORT", "3306")

BASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def dbname():
    # Each test session gets a fresh isolated database
    return "test_{}".format(binascii.b2a_hex(os.urandom(6)).decode("ascii"))


@pytest.fixture(scope="session")
async def engine(event_loop, dbname):
    # Create the test database
    base_engine = create_async_engine(f"{BASE_URL}/?charset=utf8", isolation_level="AUTOCOMMIT")
    async with base_engine.connect() as conn:
        await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {dbname}"))
    await base_engine.dispose()

    # Connect to the test database and create all tables from ORM metadata
    url = f"{BASE_URL}/{dbname}?charset=utf8"
    _engine = create_async_engine(url, echo=True)

    async with _engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield _engine

    # Teardown — drop the test database
    await _engine.dispose()
    base_engine2 = create_async_engine(f"{BASE_URL}/?charset=utf8", isolation_level="AUTOCOMMIT")
    async with base_engine2.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {dbname}"))
    await base_engine2.dispose()


@pytest.fixture()
async def dbsession(engine):
    """
    Each test gets a fresh session wrapped in a SAVEPOINT transaction
    that is rolled back after the test — no data leaks between tests.
    """
    from asyncio import current_task
    conn = await engine.connect()
    trans = await conn.begin()
    async_session = sessionmaker(conn, expire_on_commit=False, class_=AsyncSession)
    scoped = async_scoped_session(async_session, scopefunc=current_task)
    try:
        yield scoped
    finally:
        await scoped.close()
        await trans.rollback()
        await conn.close()
