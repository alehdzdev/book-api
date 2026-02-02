from datetime import datetime

# Third Party
from pymongo import MongoClient, ReturnDocument

# Local
from auth.services import get_password_hash
from config import settings

MIGRATION_NAME = "0001_initial_books_and_admin"


def migrate_initial_data():
    """
    Runs the initial data migration only once.
    Safe for Docker, reload, and multiple workers.
    """

    client = MongoClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]

    lock = db.migrations.find_one_and_update(
        {"name": MIGRATION_NAME},
        {
            "$setOnInsert": {
                "name": MIGRATION_NAME,
                "executed_at": datetime.utcnow(),
            }
        },
        upsert=True,
        return_document=ReturnDocument.BEFORE,
    )

    if lock is not None:
        print(f"[migration] {MIGRATION_NAME} already executed, skipping")
        client.close()
        return

    print(f"[migration] Running {MIGRATION_NAME}...")

    now = datetime.utcnow()

    books_data = [
        {
            "title": "Cuchillo de Agua",
            "author": "Paolo Bacigalupi",
            "published_date": datetime(2015, 5, 26),
            "genre": "Ciencia Ficción",
            "price": 19.99,
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "De animales a dioses",
            "author": "Yuval Noah Harari",
            "published_date": datetime(2011, 2, 1),
            "genre": "Historia",
            "price": 24.99,
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "published_date": datetime(1949, 6, 8),
            "genre": "Ciencia Ficción",
            "price": 15.99,
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "Metro 2033",
            "author": "Dmitry Glukhovsky",
            "published_date": datetime(2005, 11, 1),
            "genre": "Ciencia Ficción",
            "price": 12.99,
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "Los juegos del hambre",
            "author": "Suzanne Collins",
            "published_date": datetime(2008, 9, 14),
            "genre": "Ciencia Ficción",
            "price": 18.99,
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "Los juegos del hambre: En llamas",
            "author": "Suzanne Collins",
            "published_date": datetime(2009, 9, 1),
            "genre": "Ciencia Ficción",
            "price": 18.99,
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "Los juegos del hambre: Sinsajo",
            "author": "Suzanne Collins",
            "published_date": datetime(2010, 8, 24),
            "genre": "Ciencia Ficción",
            "price": 18.99,
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "El hombre más rico de Babilonia",
            "author": "George S. Clason",
            "published_date": datetime(1926, 4, 1),
            "genre": "Finanzas",
            "price": 16.99,
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "The Maze Runner: Correr o morir",
            "author": "James Dashner",
            "published_date": datetime(2009, 10, 6),
            "genre": "Ciencia Ficción",
            "price": 22.99,
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "The Maze Runner: Prueba de fuego",
            "author": "James Dashner",
            "published_date": datetime(2010, 9, 1),
            "genre": "Ciencia Ficción",
            "price": 22.99,
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "The Maze Runner: La cura mortal",
            "author": "James Dashner",
            "published_date": datetime(2011, 10, 11),
            "genre": "Ciencia Ficción",
            "price": 22.99,
            "created_at": now,
            "updated_at": now,
        },
        {
            "title": "El Código Da Vinci",
            "author": "Dan Brown",
            "published_date": datetime(2003, 3, 18),
            "genre": "Misterio",
            "price": 21.99,
            "created_at": now,
            "updated_at": now,
        },
    ]

    if books_data:
        db.books.insert_many(books_data)

    if not db.users.find_one({"username": "admin"}):
        db.users.insert_one(
            {
                "username": "admin",
                "hashed_password": get_password_hash("admin123"),
                "created_at": now,
            }
        )

    print(f"[migration] {MIGRATION_NAME} executed successfully")
    client.close()
