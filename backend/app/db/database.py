from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATA_DIR = Path(__file__).resolve().parent.parent / 'storage' / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_FILE = DATA_DIR / 'lead_the_charge.db'
DATABASE_URL = f'sqlite:///{DB_FILE}'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def session_scope() -> Session:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    from app.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
