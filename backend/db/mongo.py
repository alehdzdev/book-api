# Third Party
from pymongo import MongoClient
from pymongo.database import Database

# Local
from config import settings


class MongoDB:
    client: MongoClient = None
    database: Database = None


def connect_to_mongo():
    MongoDB.client = MongoClient(settings.MONGODB_URL)
    MongoDB.database = MongoDB.client[settings.DATABASE_NAME]
    print(f"Connected to MongoDB: {settings.DATABASE_NAME}")


def close_mongo_connection():
    if MongoDB.client:
        MongoDB.client.close()
        print("Connection to MongoDB closed")


def get_database() -> Database:
    return MongoDB.database
