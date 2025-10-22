from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent/"data"/"media_review.db"
DB_PATH.parent.mkdir(exist_ok=True, parents=True)

DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_session():
    return SessionLocal()

def init_db():
    from models import User, Media, Reviews
    Base.metadata.create_all(bind=engine)
    print("Database initialised at: ", DB_PATH)