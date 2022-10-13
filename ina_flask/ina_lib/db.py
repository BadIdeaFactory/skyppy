import datetime
from typing import Any, Dict

from sqlalchemy import JSON, Column, DateTime, Integer, String, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

DB_FILE = "sqlite:///status.db"

Base = declarative_base()


def to_dict(obj: Base) -> Dict[str, Any]:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class DbStatus(Base):
    __tablename__ = "status"
    youtube_id = Column(
        String, nullable=False, index=True, unique=True, primary_key=True
    )
    data = Column(JSON, nullable=False)


class DbStats(Base):
    __tablename__ = "statistics"
    id = Column(Integer, primary_key=True)
    url = Column(String, default="/")
    youtube_dl = Column(String, default="")
    datetime = Column(DateTime(timezone=True), default=func.now())


def create_db(file: str = DB_FILE):
    engine = create_engine(file)
    Base.metadata.create_all(engine)


engine: Engine = None
DBSession = sessionmaker()


def init_db(file: str = DB_FILE):
    engine = create_engine(file)
    Base.metadata.bind = engine
    DBSession.bind = engine


if __name__ == "__main__":
    create_db(DB_FILE)
