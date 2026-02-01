from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId

# Local
from db.mongo import get_database
from books.models import BookCreate, BookUpdate, BookInDB


class BookService:
    @staticmethod
    def _book_helper(book: Dict[str, Any]) -> BookInDB:
        book["_id"] = str(book["_id"])
        return BookInDB(**book)

    @staticmethod
    def create_book(book: BookCreate) -> BookInDB:
        db = get_database()
        book_dict = book.model_dump()
        book_dict["created_at"] = datetime.utcnow()
        book_dict["updated_at"] = datetime.utcnow()

        result = db.books.insert_one(book_dict)
        created_book = db.books.find_one({"_id": result.inserted_id})
        return BookService._book_helper(created_book)

    @staticmethod
    def get_book(book_id: str) -> Optional[BookInDB]:
        db = get_database()
        if not ObjectId.is_valid(book_id):
            return None

        book = db.books.find_one({"_id": ObjectId(book_id)})
        if book:
            return BookService._book_helper(book)
        return None

    @staticmethod
    def get_books(skip: int = 0, limit: int = 10) -> List[BookInDB]:
        db = get_database()
        books = db.books.find().skip(skip).limit(limit)
        return [BookService._book_helper(book) for book in books]

    @staticmethod
    def get_total_books() -> int:
        db = get_database()
        return db.books.count_documents({})

    @staticmethod
    def update_book(book_id: str, book_update: BookUpdate) -> Optional[BookInDB]:
        db = get_database()
        if not ObjectId.is_valid(book_id):
            return None

        update_data = book_update.model_dump(exclude_unset=True)

        if not update_data:
            return BookService.get_book(book_id)

        update_data["updated_at"] = datetime.utcnow()

        result = db.books.update_one({"_id": ObjectId(book_id)}, {"$set": update_data})

        if result.modified_count == 1:
            return BookService.get_book(book_id)
        return None

    @staticmethod
    def delete_book(book_id: str) -> bool:
        db = get_database()
        if not ObjectId.is_valid(book_id):
            return False

        result = db.books.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count == 1

    @staticmethod
    def get_average_price_by_year(year: int) -> Dict[str, Any]:
        db = get_database()

        pipeline = [
            {"$addFields": {"published_year": {"$year": "$published_date"}}},
            {"$match": {"published_year": year}},
            {
                "$group": {
                    "_id": "$published_year",
                    "average_price": {"$avg": "$price"},
                    "book_count": {"$sum": 1},
                }
            },
        ]

        result = list(db.books.aggregate(pipeline))

        if result:
            return {
                "year": year,
                "average_price": round(result[0]["average_price"], 2),
                "book_count": result[0]["book_count"],
            }
        else:
            return {"year": year, "average_price": 0.0, "book_count": 0}

    @staticmethod
    def search_books(query: str, skip: int = 0, limit: int = 10) -> List[BookInDB]:
        db = get_database()

        search_filter = {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}},
            ]
        }

        books = db.books.find(search_filter).skip(skip).limit(limit)
        return [BookService._book_helper(book) for book in books]
