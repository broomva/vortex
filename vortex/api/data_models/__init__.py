# %%
import os
from datetime import datetime
from dotenv import load_dotenv

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# from decouple import config


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


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)
    message = Column(String)
    response = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatsHistory(Base):
    __tablename__ = "chats_history"
    # id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, primary_key=True, index=True)
    history = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# %%
