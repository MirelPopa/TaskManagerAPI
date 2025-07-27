import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_HOST = os.getenv("DB_HOST", "postgres")
ADMIN_USER = os.getenv("POSTGRES_USER")
ADMIN_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_URL = os.getenv(
    "DATABASE_URL", f"postgresql://{ADMIN_USER}:{ADMIN_PASS}@{DB_HOST}:5432/{DB_NAME}"
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def create_database_schema():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
