import json
import threading
from pathlib import Path
from backend.app.schemas.book import BookData, BookResponseData, BookCreate

# Book service class loads JSON data once during application startup
class BookService:
  def __init__(self, data_path: Path) -> None:
    # Threading to prevent concurrent writes
    self._lock = threading.RLock()

    self.data_path = Path(data_path)
    self.data_path.parent.mkdir(parents=True, exist_ok=True) # To create the parent directories if they are missing

    # Creates the data JSON file if it does not already exist and initialise with an empty dictionary
    if not self.data_path.exists():
      self.data_path.write_text("{}\n", encoding="utf-8")

    # Load the data JSON file
    try:
      with self.data_path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)
    except (json.JSONDecodeError, ValueError):
      raw_data = {}

    # Checks that the JSON file is in the right format
    if not isinstance(raw_data, dict):
      raise ValueError("Data JSON must contain a JSON object keyed by book ID")

    self.books: dict[str, BookData] = raw_data

  def _save(self) -> None:
    # Create and write to temporary path first
    temp_path = self.data_path.with_suffix(self.data_path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8") as file:
      json.dump(self.books, file, indent=4, ensure_ascii=False)
      file.write("\n")

    # Replace JSON in data path with the updated data JSON
    temp_path.replace(self.data_path)

  def get_all_books(self) -> dict[str, BookResponseData]:
    with self._lock:
      return {
        book_id: {"id": book_id, **book}
        for book_id, book in self.books.items()
      }

  def get_book_by_id(self, id: str) -> BookResponseData | None:
    with self._lock:
      if id not in self.books:
        return None
      
      return {"id": id, **self.books[id]}
    
  def create_book(self, book: BookCreate) -> BookResponseData | None:
    with self._lock:
      if book.id in self.books:
        return None

      details: BookData = {
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "price": book.price
      }
      self.books[book.id] = details
      self._save()
      
      return {"id": book.id, **self.books[book.id]}

  def delete_book_by_id(self, id: str) -> bool:
    with self._lock:
      if id not in self.books:
        return False

      del self.books[id]
      self._save()

      return True

