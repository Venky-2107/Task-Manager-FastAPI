from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
import os

# Uses DATABASE_URL env variable if set (PostgreSQL on Railway),
# falls back to SQLite for local development
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")

# PostgreSQL URLs from Railway start with "postgres://" but SQLAlchemy
# needs "postgresql://" — this fixes that
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# connect_args only needed for SQLite (not PostgreSQL)
connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}

# creating the db file 
engine = create_engine('sqlite:///app.db')

# creating the local session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

# dependency injection
def get_db():
    # Create a new isolated database session for the incoming request
    db = SessionLocal()
    
    try:
        # Deliver the active database session to the path operation/route handler.
        # This pauses execution here while the API request processes.
        yield db
    finally:
        # This block executes after the API response is sent back to the user.
        # It guarantees the connection is always closed, preventing leaks.
        db.close()