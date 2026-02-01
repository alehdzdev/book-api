from typing import List

# FastAPI
from fastapi import APIRouter, HTTPException, status, Depends, Query, Path

# Local
from books.models import Book, BookCreate, BookUpdate, AveragePriceResponse
from books.services import BookService
from auth.services import get_current_user


router = APIRouter(prefix="/books", tags=["books"])


@router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def create_book(book: BookCreate):
    created_book = BookService.create_book(book)
    return created_book


@router.get("/", response_model=dict, dependencies=[Depends(get_current_user)])
async def get_books(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(
        10, ge=1, le=100, description="Cantidad de elementos por página"
    ),
):
    skip = (page - 1) * page_size
    books = BookService.get_books(skip=skip, limit=page_size)
    total = BookService.get_total_books()
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": books,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


@router.get(
    "/search", response_model=List[Book], dependencies=[Depends(get_current_user)]
)
async def search_books(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    skip = (page - 1) * page_size
    books = BookService.search_books(query=q, skip=skip, limit=page_size)
    return books


@router.get(
    "/stats/average-price/{year}",
    response_model=AveragePriceResponse,
    dependencies=[Depends(get_current_user)],
)
async def get_average_price_by_year(
    year: int = Path(..., ge=1000, le=9999, description="Año de publicación"),
):
    result = BookService.get_average_price_by_year(year)
    return result


@router.get("/{book_id}", response_model=Book, dependencies=[Depends(get_current_user)])
async def get_book(book_id: str):
    book = BookService.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {book_id} no encontrado",
        )
    return book


@router.put("/{book_id}", response_model=Book, dependencies=[Depends(get_current_user)])
async def update_book(
    book_id: str,
    book_update: BookUpdate,
):
    updated_book = BookService.update_book(book_id, book_update)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {book_id} no encontrado",
        )
    return updated_book


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
async def delete_book(book_id: str):
    deleted = BookService.delete_book(book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Libro con ID {book_id} no encontrado",
        )
    return None
