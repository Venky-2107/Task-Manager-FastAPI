from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

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