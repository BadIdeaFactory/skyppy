import datetime
from typing import Any, Dict

from ina_flask.config import option
from loguru import logger
from sqlalchemy import JSON, Column, DateTime, Integer, String, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import func

DB_FILE = option.database

Base = declarative_base()


def to_dict(obj: Base) -> Dict[str, Any]:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class DbStatus(Base):
    __tablename__ = "status"
    youtube_id = Column(
        String(250), nullable=False, index=True, unique=True, primary_key=True
    )
    data = Column(JSON, nullable=False)


class DbStats(Base):
    __tablename__ = "statistics"
    id = Column(Integer, primary_key=True)
    url = Column(String(250), default="/")
    youtube_dl = Column(String(250), default="")
    datetime = Column(DateTime(timezone=True), default=func.now())


def create_db(file: str = DB_FILE):
    engine = create_engine(file, poolclass=NullPool, isolation_level="AUTOCOMMIT")
    Base.metadata.create_all(engine)
    logger.debug(engine)


engine: Engine = None
DBSession = sessionmaker()


def init_db(file: str = DB_FILE):
    engine = create_engine(file, poolclass=NullPool, isolation_level="AUTOCOMMIT")
    Base.metadata.bind = engine
    DBSession.bind = engine


if __name__ == "__main__":
    create_db(DB_FILE)
