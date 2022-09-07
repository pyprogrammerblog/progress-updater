from updater.utils import progress_updater
from sqlmodel import select
from updater.backends.sql import SQLSettings, SQLLog
from updater.backends.mongo import MongoSettings
from updater.backends.redis import RedisSettings


def test_progress_updater_passing_params_redis(redis_backend, capsys):

    redis_settings = RedisSettings(
        redis_password="pass", redis_host="redis", redis_db=1
    )

    @progress_updater(
        verbose=True,
        task_name="My task",
        settings=redis_settings,
    )
    def task():
        return "doing a lot of work..."

    assert not redis_backend.keys()
    assert capsys.readouterr().out == ""

    task()  # run the task

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\t\tTime spent: "
        "0h0m\t\tSuccessfully completed"
    )
    assert redis_backend.keys()


def test_progress_updater_passing_params_mongo(mongo_backend, capsys):

    mongo_settings = MongoSettings(
        mongo_connection="mongodb://user:pass@mongo:27017",
        mongo_db="db",
        mongo_collection="logs",
    )

    @progress_updater(
        verbose=True,
        task_name="My task",
        settings=mongo_settings,
    )
    def task():
        return "doing a lot of work..."

    assert not mongo_backend.count_documents(filter={})
    assert capsys.readouterr().out == ""

    task()  # run the task

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\t\tTime spent: "
        "0h0m\t\tSuccessfully completed"
    )
    assert mongo_backend.count_documents(filter={})


def test_progress_updater_passing_params_sql(sql_backend, capsys):

    sql_settings = SQLSettings(
        sql_dsn="postgresql+psycopg2://user:pass@postgres:5432/db",
        sql_table="logs",
    )

    @progress_updater(
        verbose=True,
        task_name="My task",
        settings=sql_settings,
    )
    def task():
        return "doing a lot of work..."

    assert not sql_backend.exec(select(SQLLog)).first()
    assert capsys.readouterr().out == ""

    task()  # run the task

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\t\tTime spent: "
        "0h0m\t\tSuccessfully completed"
    )
    assert sql_backend.exec(select(SQLLog)).first()


# env vars
def test_progress_updater_env_vars_redis(
    redis_backend, env_vars_redis, capsys
):
    @progress_updater(
        verbose=True,
        task_name="My task",
    )
    def task():
        return "doing a lot of work..."

    assert not redis_backend.keys()
    assert capsys.readouterr().out == ""

    task()  # run the task

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\t\tTime spent: "
        "0h0m\t\tSuccessfully completed"
    )
    assert redis_backend.keys()


def test_progress_updater_env_vars_mongo(
    mongo_backend, env_vars_mongo, capsys
):
    @progress_updater(
        verbose=True,
        task_name="My task",
    )
    def task():
        return "doing a lot of work..."

    assert not mongo_backend.count_documents(filter={})
    assert capsys.readouterr().out == ""

    task()  # run the task

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\t\tTime spent: "
        "0h0m\t\tSuccessfully completed"
    )
    assert mongo_backend.count_documents(filter={})


def test_progress_updater_env_vars_sql(sql_backend, env_vars_sql, capsys):
    @progress_updater(
        verbose=True,
        task_name="My task",
    )
    def task():
        return "doing a lot of work..."

    assert not sql_backend.exec(select(SQLLog)).first()
    assert capsys.readouterr().out == ""

    task()  # run the task

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\t\tTime spent: "
        "0h0m\t\tSuccessfully completed"
    )
    assert sql_backend.exec(select(SQLLog)).first()
