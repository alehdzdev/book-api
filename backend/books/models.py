from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId

# Third Party
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class BookBase(BaseModel):
    title: str = Field(
        ..., description="Título del libro", min_length=1, max_length=200
    )
    author: str = Field(
        ..., description="Autor del libro", min_length=1, max_length=100
    )
    published_date: datetime = Field(..., description="Fecha de publicación")
    genre: str = Field(..., description="Género literario", min_length=1, max_length=50)
    price: float = Field(..., description="Precio del libro", gt=0)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    published_date: Optional[datetime] = None
    genre: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0)


class BookInDB(BookBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


class Book(BookInDB):
    pass


class AveragePriceResponse(BaseModel):
    year: int
    average_price: float
    book_count: int
