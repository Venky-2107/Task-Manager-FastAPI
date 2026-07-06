from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_db, Base
from main import app
import pytest

# !! NEVER use production DB URL here !!
# Separate test DB ensures tests don't affect real data
TEST_DB_URL = "sqlite:///test.db"

# Create a separate engine pointing to test DB
# Same as database.py but for testing only
test_engine = create_engine(TEST_DB_URL)

# Session factory for test DB
# Same config as SessionLocal in database.py
Test_Session_Local = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)

def override_get_db():
    """
    Replacement for get_db dependency during tests.
    FastAPI will use this instead of the real get_db,
    so all DB operations go to test.db instead of app.db
    """
    db = Test_Session_Local()
    try:
        yield db
    finally:
        db.close()

# Swap the real get_db with test version
# All routes that use Depends(get_db) will now use test DB
app.dependency_overrides[get_db] = override_get_db

Base.metadata.drop_all(bind=test_engine)
Base.metadata.create_all(bind=test_engine)

# Shared test client — simulates HTTP requests without running a server
# Import this in every test file instead of creating a new one
client = TestClient(app)

@pytest.fixture(autouse=True, scope="session")
def reset_db():
    """
    Runs ONCE before all tests in the session.
    - drop_all: wipes all tables (clean slate)
    - create_all: recreates tables from models
    - yield: tests run here
    scope="session" means tests can share data across files
    (e.g. test_tasks.py can use user created in test_auth.py)
    """
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
