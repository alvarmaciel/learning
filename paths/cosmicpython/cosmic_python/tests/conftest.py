import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from allocator.infrastructure.orm import metadata, start_mappers

@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:", echo=True)  # Debugging SQL execution
    metadata.create_all(engine)
    return engine

@pytest.fixture
def session(in_memory_db):
    clear_mappers()
    start_mappers()
    Session = sessionmaker(bind=in_memory_db)
    session = Session()

    try:
        yield session
        session.commit()
    finally:
        session.rollback()
        session.close()
        clear_mappers()
