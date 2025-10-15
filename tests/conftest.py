import pytest
import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import create_app
from app.database import Base, get_db

# Create a temporary database for testing
@pytest.fixture(scope="session")
def temp_db():
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    
    # Create engine and session
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    yield TestingSessionLocal, engine
    
    # Cleanup
    os.unlink(db_path)

@pytest.fixture
def db_session(temp_db):
    TestingSessionLocal, engine = temp_db
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_movie():
    return {
        "title": "The Matrix",
        "director": "The Wachowskis",
        "year": 1999,
        "rating": 8.7
    }

@pytest.fixture
def sample_movies():
    return [
        {
            "title": "The Matrix",
            "director": "The Wachowskis", 
            "year": 1999,
            "rating": 8.7
        },
        {
            "title": "Inception",
            "director": "Christopher Nolan",
            "year": 2010,
            "rating": 8.8
        },
        {
            "title": "Interstellar",
            "director": "Christopher Nolan",
            "year": 2014,
            "rating": 8.6
        }
    ]