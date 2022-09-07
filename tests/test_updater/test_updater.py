from sqlmodel import select
from updater import ProgressUpdater
from updater.backends.sql import SQLSettings, SQLLog
from updater.backends.mongo import MongoSettings
from updater.backends.redis import RedisSettings


def test_progress_updater_skip_backend(mongo_backend, capsys):

    assert not mongo_backend.count_documents(filter={})
    assert capsys.readouterr().out == ""

    updater = ProgressUpdater(
        task_name="My Task",
        write_on_backend=False,
    )

    with updater(block_name="First Block") as updater:
        updater.notify("Doing first block...")

    with updater(block_name="Second Block") as updater:
        updater.notify("Doing second block...")

    updater.raise_latest_exception()

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\tDoing first block..."
        "\t\tTime spent: 0h0m\t\tSuccessfully completed\t- Entering ..."
        "\tDoing second block...\t\t"
        "Time spent: 0h0m\t\tSuccessfully completed"
    )
    assert not mongo_backend.count_documents(filter={})


def test_progress_updater_skip_backend_no_verbose(mongo_backend, capsys):

    assert not mongo_backend.count_documents(filter={})
    assert capsys.readouterr().out == ""

    updater = ProgressUpdater(
        task_name="My Task", write_on_backend=False, verbose=False
    )

    with updater(block_name="First Block") as updater:
        updater.notify("Doing first block...")

    updater.raise_latest_exception()

    assert capsys.readouterr().out == ""
    assert not mongo_backend.count_documents(filter={})


def test_progress_updater_skip_backend_raise_exception(mongo_backend, capsys):

    assert not mongo_backend.count_documents(filter={})
    assert capsys.readouterr().out == ""

    updater = ProgressUpdater(task_name="My Task", write_on_backend=False)

    with updater(block_name="First Block") as updater:
        updater.notify("Doing first block...")
        1 / 0

    try:
        updater.raise_latest_exception()
    except Exception as e:
        assert isinstance(e, ZeroDivisionError)

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\tDoing first block..."
        "\t\tTime spent: 0h0m\t\tFailed\t\tError message: "
        "<class 'ZeroDivisionError'>: division by zero"
    )
    assert not mongo_backend.count_documents(filter={})


def test_progress_updater_raise_exception(mongo_backend, capsys):

    assert not mongo_backend.count_documents(filter={})
    assert capsys.readouterr().out == ""

    updater = ProgressUpdater(
        task_name="My Task",
        settings=MongoSettings(
            mongo_connection="mongodb://user:pass@mongo:27017",
            mongo_db="db",
            mongo_collection="logs",
        ),
    )

    with updater(block_name="First Block") as updater:
        updater.notify("Doing first block...")
        1 / 0

    try:
        updater.raise_latest_exception()
    except Exception as e:
        assert isinstance(e, ZeroDivisionError)

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\tDoing first block..."
        "\t\tTime spent: 0h0m\t\tFailed\t\tError message: "
        "<class 'ZeroDivisionError'>: division by zero"
    )
    assert mongo_backend.count_documents(filter={})


def test_progress_updater_passing_params_redis(redis_backend, capsys):

    assert not redis_backend.keys()
    assert capsys.readouterr().out == ""

    redis_settings = RedisSettings(
        redis_password="pass", redis_host="redis", redis_db=1
    )

    updater = ProgressUpdater(task_name="My Task", settings=redis_settings)

    with updater(block_name="First Block") as updater:
        updater.notify("Doing first block...")

    with updater(block_name="Second Block") as updater:
        updater.notify("Doing second block...")

    updater.raise_latest_exception()

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\tDoing first block..."
        "\t\tTime spent: 0h0m\t\tSuccessfully completed\t- Entering ..."
        "\tDoing second block...\t\t"
        "Time spent: 0h0m\t\tSuccessfully completed"
    )
    assert redis_backend.keys()


def test_progress_updater_passing_params_mongo(mongo_backend, capsys):

    updater = ProgressUpdater(
        task_name="My Task",
        settings=MongoSettings(
            mongo_connection="mongodb://user:pass@mongo:27017",
            mongo_db="db",
            mongo_collection="logs",
        ),
    )

    with updater(block_name="First Block") as updater:
        updater.notify("Doing first block...")

    with updater(block_name="Second Block") as updater:
        updater.notify("Doing second block...")

    updater.raise_latest_exception()

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\tDoing first block..."
        "\t\tTime spent: 0h0m\t\tSuccessfully completed\t- Entering ..."
        "\tDoing second block...\t\t"
        "Time spent: 0h0m\t\tSuccessfully completed"
    )
    assert mongo_backend.count_documents(filter={})


def test_progress_updater_passing_params_sql(sql_backend, capsys):

    assert not sql_backend.exec(select(SQLLog)).first()

    sql_settings = SQLSettings(
        sql_dsn="postgresql+psycopg2://user:pass@postgres:5432/db",
        sql_table="logs",
    )

    updater = ProgressUpdater(task_name="My Task", settings=sql_settings)

    with updater(block_name="First Block") as updater:
        updater.notify("Doing first block...")

    with updater(block_name="Second Block") as updater:
        updater.notify("Doing second block...")

    updater.raise_latest_exception()

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\tDoing first block..."
        "\t\tTime spent: 0h0m\t\tSuccessfully completed\t- Entering ..."
        "\tDoing second block...\t\t"
        "Time spent: 0h0m\t\tSuccessfully completed"
    )
    assert sql_backend.exec(select(SQLLog)).first()


# env vars
def test_progress_updater_env_vars_redis(
    redis_backend, env_vars_redis, capsys
):

    assert not redis_backend.keys()

    updater = ProgressUpdater(task_name="My Task")

    with updater(block_name="First Block") as updater:
        updater.notify("Doing first block...")

    with updater(block_name="Second Block") as updater:
        updater.notify("Doing second block...")

    updater.raise_latest_exception()

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\tDoing first block..."
        "\t\tTime spent: 0h0m\t\tSuccessfully completed\t- Entering ..."
        "\tDoing second block...\t\t"
        "Time spent: 0h0m\t\tSuccessfully completed"
    )
    assert redis_backend.keys()


def test_progress_updater_env_vars_mongo(
    mongo_backend, env_vars_mongo, capsys
):

    assert not mongo_backend.count_documents(filter={})

    updater = ProgressUpdater(task_name="My Task")

    with updater(block_name="First Block") as updater:
        updater.notify("Doing first block...")

    with updater(block_name="Second Block") as updater:
        updater.notify("Doing second block...")

    updater.raise_latest_exception()

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\tDoing first block..."
        "\t\tTime spent: 0h0m\t\tSuccessfully completed\t- Entering ..."
        "\tDoing second block...\t\t"
        "Time spent: 0h0m\t\tSuccessfully completed"
    )
    assert mongo_backend.count_documents(filter={})


def test_progress_updater_env_vars_sql(sql_backend, env_vars_sql, capsys):

    assert not sql_backend.exec(select(SQLLog)).first()

    updater = ProgressUpdater(task_name="My Task")

    with updater(block_name="First Block") as updater:
        updater.notify("Doing first block...")

    with updater(block_name="Second Block") as updater:
        updater.notify("Doing second block...")

    updater.raise_latest_exception()

    assert (
        capsys.readouterr().out
        == "\t- Task: My task\t- Entering ...\tDoing first block..."
        "\t\tTime spent: 0h0m\t\tSuccessfully completed\t- Entering ..."
        "\tDoing second block...\t\t"
        "Time spent: 0h0m\t\tSuccessfully completed"
    )
    assert sql_backend.exec(select(SQLLog)).first()
