from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, Response, Depends, status, Path

from backend.app.schemas.book import BookCreate, BookResponse
from backend.app.services.book_service import BookService

router = APIRouter(prefix="/api/book", tags=["books"])

BookId = Annotated[
    str,
    Path(min_length=4, max_length=100, pattern=r"^B")
]

def get_book_service(request: Request) -> BookService:
  return request.app.state.book_service

@router.get("/", response_model=dict[str, BookResponse], status_code=status.HTTP_200_OK)
def get_books(service: BookService = Depends(get_book_service)):
  return service.get_all_books() 

@router.get("/{id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book(id: BookId, service: BookService = Depends(get_book_service)):
  book = service.get_book_by_id(id)
  if book is None:
    raise HTTPException(status_code=404, detail=f"Book with id {id} not found.")
  
  return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate, service: BookService = Depends(get_book_service)):
  book_obj = service.create_book(book)
  if book_obj is None:
    raise HTTPException(status_code=409, detail=f"Book with id {book.id} already exists.")

  return book_obj

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: BookId, service: BookService = Depends(get_book_service)):
  is_deleted = service.delete_book_by_id(id)
  if not is_deleted:
    raise HTTPException(status_code=404, detail=f"Book with id {id} not found.")

  return Response(status_code=status.HTTP_204_NO_CONTENT)