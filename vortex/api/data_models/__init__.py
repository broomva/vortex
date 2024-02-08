# %%
import os

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

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


Base.metadata.create_all(engine)
# %%
