import uuid
from updater.backends import Settings
from sqlmodel import select
from updater.backends.sql import SQLSettings, SQLLog


def test_create_settings_passing_params_sql(sql_backend):

    sql_settings = SQLSettings(
        sql_dsn="postgresql+psycopg2://user:pass@postgres:5432/db",
        sql_table="logs",
    )
    klass = sql_settings.backend()
    log: SQLLog = klass(task_name="My task")

    statement = select(SQLLog).where(SQLLog.uuid == log.uuid)
    assert not sql_backend.exec(statement).first()

    log.description = "A description"
    log = log.save()
    log = SQLLog.get(uuid=log.uuid)

    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)
    assert sql_backend.query(SQLLog).filter_by(uuid=log.uuid)
    assert 1 == log.delete()
    assert not sql_backend.query(SQLLog).filter_by(uuid=log.uuid)
    assert 0 == log.delete()


def test_create_settings_env_vars_sql(sql_backend, env_vars_sql):

    settings = Settings()
    klass = settings.backend()
    log: SQLLog = klass(task_name="My task")

    assert not sql_backend.query(SQLLog).filter_by(uuid=log.uuid)

    log.description = "A description"
    log = log.save()
    log = SQLLog.get(uuid=log.uuid)

    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)
    assert sql_backend.query(SQLLog).filter_by(uuid=log.uuid)
    assert 1 == log.delete()
    assert not sql_backend.query(SQLLog).filter_by(uuid=log.uuid)
    assert 0 == log.delete()
