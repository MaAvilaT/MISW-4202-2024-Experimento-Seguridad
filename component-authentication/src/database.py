import os

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


if os.environ.get('DATABASE_URL'):
    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ.get('DATABASE_USER', 'maat'),
        password=os.environ.get('DATABASE_PASSWORD', 'SECURE&STRING_PASSWORD'),
        host=os.environ.get('DATABASE_HOSTNAME', 'localhost'),
        port=os.environ.get('DATABASE_PORT', '5432'),
        database=os.environ.get('DATABASE_NAME', 'component_authentication_database'),
    )
else:
    connection_url = 'sqlite:///./component-authentication.db'

engine = create_engine(connection_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def yield_db_session() -> SessionLocal:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

