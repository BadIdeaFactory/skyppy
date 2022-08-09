from typing import Any, Dict

from config import option
from sqlalchemy import JSON, Column, Integer, String, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = option.db_url

Base = declarative_base()


def to_dict(obj: Base) -> Dict[str, Any]:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class DbStatus(Base):
    __tablename__ = "status"
    youtube_id = Column(
        String(255), nullable=False, index=True, unique=True, primary_key=True
    )
    data = Column(JSON, nullable=False)


def create_db(file: str = DB_URL):
    engine = create_engine(file)
    Base.metadata.create_all(engine)


engine: Engine = None
DBSession = sessionmaker()


def init_db(file: str = DB_URL):
    if option.deploy == "LOCAL_MACHINE":
        engine = create_engine(file)
        Base.metadata.bind = engine
        DBSession.bind = engine
    if option.deploy == "WEB":
        engine = create_engine(file, pool_recycle=3600, pool_size=10)
        Base.metadata.bind = engine
        DBSession.bind = engine


if __name__ == "__main__":
    create_db(DB_URL)
