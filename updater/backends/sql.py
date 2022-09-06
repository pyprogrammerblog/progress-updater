import logging
from typing import Dict
from sqlmodel import Session, SQLModel, create_engine, select, Field
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from updater.backends.log import Log
from contextlib import contextmanager


__all__ = ["SQLLog", "SQLSettings"]


logger = logging.getLogger(__name__)


class SQLLog(Log, SQLModel):
    """
    SQL Log
    """

    class Meta:
        sql_dsn: str
        sql_table: str

    @classmethod
    @contextmanager
    def sql_session(cls) -> Session:
        """
        Yield a connection
        """
        engine = create_engine(cls.Meta.sql_dsn)
        with Session(engine) as session:
            yield session

    @classmethod
    def get(cls, uuid: UUID):
        """
        Get object from DataBase
        """
        with cls.sql_session() as session:
            statement = select(cls).where(cls.uuid == uuid)
            if task := session.exec(statement).first():
                return task

    def save(self):
        """
        Updates object in DataBase
        """
        self.updated = datetime.utcnow()
        with self.sql_session() as session:
            session.add(self)
            session.commit()
        return self

    def delete(self):
        """
        Deletes object in DataBase
        """
        with self.sql_session() as session:
            session.delete(self)
            session.commit()


class SQLSettings(BaseModel):
    sql_dsn: str
    sql_table: str = "Logs"
    sql_extras: Dict = None

    def backend(self):
        SQLLog.Meta.sql_dsn = self.sql_dsn
        SQLLog.Meta.sql_table = self.sql_table
        return SQLLog
