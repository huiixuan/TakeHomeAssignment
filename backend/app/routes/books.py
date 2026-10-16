from fastapi import APIRouter, HTTPException
from backend.app.schemas.book import BookCreate, BookResponse
from backend.app.services.book_service import get_all_books, get_book_by_id, create_book, delete_book_by_id

router = APIRouter(prefix="/api/book", tags=["books"])

@router.get("/", response_model=dict[str, BookResponse], status_code=200)
def get_books():
  books = get_all_books()

  return {
    book_id: {"id": book_id, **book}
    for book_id, book in books.items()
  }

@router.get("/{id}", response_model=BookResponse, status_code=200)
def get_book(id: str):
  book = get_book_by_id(id)
  if book is None:
    raise HTTPException(status_code=404, detail=f"Book with id {id} not found.")
  
  return book

@router.post("/", response_model=BookResponse, status_code=201)
def add_book(book: BookCreate):
  book_obj = create_book(book)
  if book_obj is None:
    raise HTTPException(status_code=409, detail=f"Book with id {book.id} already exists.")

  return book_obj

@router.delete("/{id}", status_code=204)
def delete_book(id: str):
  deleted_id = delete_book_by_id(id)
  if deleted_id is None:
    raise HTTPException(status_code=404, detail=f"Book with id {id} not found.")

