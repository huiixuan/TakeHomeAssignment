import json
from pathlib import Path
from backend.app.schemas.book import BookCreate

BOOKS_DATA = Path(__file__).resolve().parent.parent / "data" / "books.json"

def get_all_books():
  with open(BOOKS_DATA, "r") as f:
    return json.load(f)

def get_book_by_id(id: str):
  books = get_all_books()
  return (
    {"id": id, **books.get(id)}
    if id in books else None
  )

def create_book(book: BookCreate):
  books = get_all_books()
  if book.id in books:
    return None

  books[book.id] = book.model_dump(exclude={"id"})

  with open(BOOKS_DATA, "w") as f:
    json.dump(books, f, indent=4)

  return {"id": book.id, **books[book.id]}

def delete_book_by_id(id: str):
  books = get_all_books()
  if id not in books:
    return None

  del books[id]
  with open(BOOKS_DATA, "w") as f:
    json.dump(books, f, indent=4)

  return id

