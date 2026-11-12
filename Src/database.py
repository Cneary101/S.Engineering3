from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'newsagent.db')}"

engine = create_engine(DATABASE_URL)

@event.listens_for(engine, "connect")
def _enable_sqlite_fks(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Base = declarative_base()