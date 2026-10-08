from sqlmodel import create_engine, Session
from app.core.config import settings

# SQLite requires this flag to allow multiple threads to interact with the connection
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

# Create the SQLAlchemy/SQLModel engine
engine = create_engine(
    settings.DATABASE_URL, 
    echo=False,  # Set to True to see SQL queries in the console
    connect_args=connect_args
)

def get_session():
    """
    Dependency generator that yields a database session.
    Used in FastAPI routes to handle database connections safely.
    """
    with Session(engine) as session:
        yield session