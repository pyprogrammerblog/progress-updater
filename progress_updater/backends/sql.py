import logging
from typing import Dict, List, Union
from sqlmodel import Session, SQLModel, create_engine, select, Field
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from uuid import uuid4
from contextlib import contextmanager
from progress_updater.backends.log import BaseLog


__all__ = ["SQLLog", "SQLSettings"]


logger = logging.getLogger(__name__)


class SQLLog(BaseLog, SQLModel, table=True):  # type: ignore
    """
    SQLLog class. Defines the Log for SQL Backend

    Usage:

        >>> from progress_updater.backends import SQLSettings
        >>>
        >>> settings = SQLSettings(
        >>>     sql_dsn="postgresql+psycopg2://user:pass@postgres:5432/db"
        >>> )
        >>> SQLLog = SQLSettings.backend()  # type: Type[SQLLog]
        >>> log = SQLLog(task_name="My task", description="A cool task")
        >>> log.save()
        >>>
        >>> assert log.dict() == {"task_name": "My task", ...}
        >>> assert log.json() == '{"task_name": "My task", ...}'
        >>>
        >>> log = SQLLog.get(uuid=UUID("<your-uuid>"))
        >>> assert log.description == "A cool task"
        >>>
        >>> assert log.delete() == 1
    """

    __tablename__ = "progress_updater_logs"

    uuid: UUID = Field(default_factory=uuid4, primary_key=True)

    class Meta:
        sql_dsn: str

    @classmethod
    @contextmanager
    def sql_session(cls):
        """
        Yield a connection
        """
        assert cls.Meta.sql_dsn, "Please set a sql dsn string"

        engine = create_engine(cls.Meta.sql_dsn)
        with Session(engine) as session:
            yield session

    @classmethod
    def get(cls, uuid: UUID) -> Union["SQLLog", None]:
        """
        Get object from DataBase

        Usage:

            >>> ...
            >>> log = SQLLog.get(uuid=UUID("<your-uuid>"))
            >>> assert log.uuid == UUID("<your-uuid>")
            >>>
        """
        with cls.sql_session() as session:  # type: Session
            statement = select(cls).where(cls.uuid == str(uuid))
            if task := session.exec(statement).first():
                return task
            return None

    def save(self) -> "SQLLog":
        """
        Updates/Creates object in DataBase

        Usage:

            >>> ...
            >>> log = SQLLog(task_name="My Task")
            >>> log.save()
            >>> log.description = "A new description"
            >>> log.save()
            >>> ...
        """
        self.updated = datetime.utcnow()
        with self.sql_session() as session:
            session.add(self)
            session.commit()
            session.refresh(self)
        return self

    def delete(self) -> int:
        """
        Deletes object in DataBase

        Usage:

            >>> ...
            >>> assert log.delete() == 1  # count deleted 1
            >>> assert log.delete() == 0  # count deleted 0
            >>> ...
        """
        with self.sql_session() as session:
            statement = select(SQLLog).where(self.uuid == self.uuid)
            if task := session.exec(statement).first():
                session.delete(task)
                session.commit()
                return 1
            return 0


class SQLSettings(BaseModel):
    """
    SQL Settings. Returns a SQLLog class and set SQL backend settings

    Usage:

        >>> from progress_updater.backends import SQLSettings
        >>>
        >>> settings = SQLSettings(
        >>>     sql_dsn="postgresql+psycopg2://user:pass@postgres:5432/db"
        >>> )
        >>> SQLLog = SQLSettings.backend()  # type: Type[SQLLog]
        >>> log = SQLLog(task_name="My task", description="A cool task")
        >>> log.save()
    """

    sql_dsn: str = Field(..., description="SQLAlchemy dsn connection")
    sql_table: str = Field(
        default="progress_updater_logs", description="Table name"
    )
    sql_extras: Dict = Field(
        default_factory=dict, description="SQLAlchemy extras"
    )

    def backend(self):
        SQLLog.Meta.sql_dsn = self.sql_dsn
        SQLLog.Meta.sql_extras = self.sql_extras
        SQLLog.__tablename__ = self.sql_table
        return SQLLog


class SQLLogs(BaseModel):
    """
    Defines the SQL Logs collection
    """

    logs: List[SQLLog] = Field(default_factory=list, description="Logs")
    count: int = Field(default=0, description="Count")
