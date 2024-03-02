# %%
import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

url = URL.create(
    drivername="postgresql",
    username=os.environ.get("POSTGRES_USERNAME"),  # config("DB_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),  # config("DB_PASSWORD"),
    host=os.environ.get("POSTGRES_HOST"),
    database=os.environ.get("POSTGRES_DATABASE"),
    port=os.environ.get("POSTGRES_PORT"),
)

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    """
    Returns a database session.

    Yields:
        SessionLocal: The database session.

    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    """
    Context manager wrapper for the get_db generator.
    """
    try:
        db = next(get_db())  # Get the session from the generator
        yield db
    finally:
        db.close()