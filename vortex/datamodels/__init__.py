# %%
import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

engine = create_engine(os.environ.get("SQLALCHEMY_URL"))
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
