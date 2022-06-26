import os, logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# the secret configuration specific things
from config import Config


LOGS = logging.getLogger(__name__)

Config.DB_URI = Config.get("DB_URI")
def start() -> scoped_session:
    database_url = (
        Config.get("DB_URI").replace("postgres:", "postgresql:")
        if "postgres://" in Config.get("DB_URI")
        else Config.get("DB_URI")
    )
    engine = create_engine(database_url)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    BASE = declarative_base()
    SESSION = start()
except AttributeError as e:
    # this is a dirty way for the work-around required for #23
    LOGS.error(
        "DB_URI is not configured. Features depending on the database might have issues."
    )
    LOGS.error(str(e))
