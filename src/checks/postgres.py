from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text

from infrastructure.logger import create_logger
from infrastructure.settings import Settings

LOGGER = create_logger(__name__)
SQLALCHEMY_DATABASE_URL = Settings.load().postgres.url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def check_postgres_health(session: Session):
    log = LOGGER.getChild("check_postgres_health")
    log.info("Checking postgres health")
    is_database_working = True
    error = None

    try:
        # to check database we will execute raw query
        session.execute(text("SELECT 1"))
    except Exception as e:
        error = str(e)
        log.error(f"Error checking postgres health: {error}")
        is_database_working = False

    return is_database_working, error


def get_postgres_session():
    log = LOGGER.getChild("get_postgres_session")
    log.info("Getting postgres session")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
