from pymongo import MongoClient
from src.core.config import mongo_config

client = MongoClient(host=mongo_config.host, port=mongo_config.port)


def init_db():
    db = client[mongo_config.db_name]
    return db
