import uuid
from pymongo import MongoClient
from updater.backends import Settings
from updater.backends.mongo import MongoSettings, MongoLog


def test_create_settings_passing_params_mongo(drop_mongo):

    mongo_settings = MongoSettings(
        mongo_connection="mongodb://user:pass@mongo:27017",
        mongo_db="db",
        mongo_collection="logs",
    )
    klass = mongo_settings.backend()
    log: MongoLog = klass(task_name="My task")

    with MongoClient(
        "mongodb://user:pass@mongo:27017", UuidRepresentation="standard"
    ) as client:
        db = client.get_database("db")
        collection = db.get_collection("logs")
        assert 0 == collection.count_documents(filter={})

    log.description = "A description"
    log = log.save()
    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)

    with MongoClient(
        "mongodb://user:pass@mongo:27017", UuidRepresentation="standard"
    ) as client:
        db = client.get_database("db")
        collection = db.get_collection("logs")
        assert 1 == collection.count_documents(filter={})

    log.delete()

    with MongoClient(
        "mongodb://user:pass@mongo:27017", UuidRepresentation="standard"
    ) as client:
        db = client.get_database("db")
        collection = db.get_collection("logs")
        assert 0 == collection.count_documents(filter={})


def test_create_settings_env_vars_mongo(drop_mongo, env_vars_mongo):

    settings = Settings()
    klass = settings.backend()
    log = klass(task_name="My task")

    with MongoClient(
        "mongodb://user:pass@mongo:27017", UuidRepresentation="standard"
    ) as client:
        db = client.get_database("db")
        collection = db.get_collection("logs")
        assert 0 == collection.count_documents(filter={})

    log.description = "A description"
    log = log.save()
    assert log.description == "A description"
    assert isinstance(log.uuid, uuid.UUID)

    with MongoClient(
        "mongodb://user:pass@mongo:27017", UuidRepresentation="standard"
    ) as client:
        db = client.get_database("db")
        collection = db.get_collection("logs")
        assert 1 == collection.count_documents(filter={})

    log.delete()

    with MongoClient(
        "mongodb://user:pass@mongo:27017", UuidRepresentation="standard"
    ) as client:
        db = client.get_database("db")
        collection = db.get_collection("logs")
        assert 0 == collection.count_documents(filter={})
