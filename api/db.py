import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_HOST = os.getenv("DB_HOST", "postgres")
ADMIN_USER = os.getenv("POSTGRES_USER")
ADMIN_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_URL = os.getenv(
    "DATABASE_URL", f"postgresql://{ADMIN_USER}:{ADMIN_PASS}@{DB_HOST}:5432/{DB_NAME}"
)

Base = declarative_base()


def create_database_schema(engine: Engine | None = None):
    engine = engine or get_engine()
    Base.metadata.create_all(bind=engine)


def get_engine(db_url: str | None = None):
    if not db_url:
        db_host = os.getenv("DB_HOST", "localhost")
        user = os.getenv("POSTGRES_USER", "admin_user")
        password = os.getenv("POSTGRES_PASSWORD", "admin_pass")
        db_name = os.getenv("POSTGRES_DB", "task_manager_api_db")
        db_url = f"postgresql://{user}:{password}@{db_host}:5432/{db_name}"

    return create_engine(db_url)


def get_session_local(db_url: str | None = None):
    engine = get_engine(db_url)
    return sessionmaker(bind=engine)


def get_db(db_url: str | None = None):
    SessionLocal = get_session_local(db_url)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
