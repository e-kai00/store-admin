from collections.abc import Iterator
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from app.config import settings

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.postgres_user,
    password=settings.postgres_password,
    host="localhost",
    port=settings.postgres_port,
    database=settings.postgres_db,
)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    database_session = Session(
        bind=engine,
        expire_on_commit=False,
    )
    try:
        yield database_session
    finally:
        database_session.close()
