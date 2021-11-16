import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.configs.data_source_configs import END_POINT, AUTHORIZATION, SERVICE_KEY
from src.configs.database import Base
from src.trials.infra.orm import Trial

pytest_plugins = [
    "tests.fixtures.data",
]

TEST_SQLITE_URL = "sqlite:///:memory:"


@pytest.fixture
def rest_authentication():
    return {
        "url": END_POINT,
        "authorization": AUTHORIZATION,
        "service_key": SERVICE_KEY
    }


@pytest.fixture
def in_memory_db():
    engine = create_engine(TEST_SQLITE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db):
    yield sessionmaker(bind=in_memory_db)
    Base.metadata.drop_all(bind=in_memory_db)
