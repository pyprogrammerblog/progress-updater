import uuid
from updater.backends import Settings
from updater.backends.mongo import MongoSettings, MongoLog


def test_create_settings_passing_params_mongo(mongo_backend):

    mongo_settings = MongoSettings(
        mongo_connection="mongodb://user:pass@mongo:27017",
        mongo_db="db",
        mongo_collection="logs",
    )
    klass = mongo_settings.backend()
    log: MongoLog = klass(task_name="My task")

    db = mongo_backend.get_database("db")
    collection = db.get_collection("logs")
    assert 0 == collection.count_documents(filter={})

    log.description = "A description"
    log = log.save()
    log = MongoLog.get(uuid=log.uuid)

    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)
    assert 1 == collection.count_documents(filter={})
    assert 1 == log.delete()
    assert 0 == collection.count_documents(filter={})
    assert 0 == log.delete()


def test_create_settings_env_vars_mongo(mongo_backend, env_vars_mongo):

    settings = Settings()
    klass = settings.backend()
    log = klass(task_name="My task")

    db = mongo_backend.get_database("db")
    collection = db.get_collection("logs")
    assert 0 == collection.count_documents(filter={})

    log.description = "A description"
    log = log.save()
    log = MongoLog.get(uuid=log.uuid)

    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)
    assert 1 == collection.count_documents(filter={})
    assert 1 == log.delete()
    assert 0 == collection.count_documents(filter={})
    assert 0 == log.delete()
