import json
import tempfile
import unittest
from pathlib import Path
from backend.app.schemas.book import BookCreate
from backend.app.services.book_service import BookService


class TestBookService(unittest.TestCase):
  def setUp(self):
    # Set up temporary directory for dummy book data
    self.temp_dir = tempfile.TemporaryDirectory()
    self.data_file = Path(self.temp_dir.name) / "books.json"

    self.initial_books = {
      "B001": {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "genre": "Software Engineering",
        "price": 45.0,
      }
    }

    self.data_file.write_text(json.dumps(self.initial_books))
    self.service = BookService(self.data_file)

  def tearDown(self):
    self.temp_dir.cleanup()

  def read_saved_books(self):
    with open(self.data_file, "r") as f:
      return json.load(f)

  def make_book(self, book_id="B002"):
    return BookCreate(
      id=book_id,
      title="The Pragmatic Programmer",
      author="Andrew Hunt",
      genre="Programming",
      price=50.0,
    )

  def test_get_all_books(self):
    books = self.service.get_all_books()
    self.assertIn("B001", books)
    self.assertEqual(books["B001"]["title"], "Clean Code")

  def test_get_existing_book(self):
    book = self.service.get_book_by_id("B001")
    self.assertIsNotNone(book)
    assert book is not None

    self.assertEqual(book["title"], "Clean Code")
    self.assertEqual(book["author"], "Robert C. Martin")

  def test_get_nonexistent_book(self):
    book = self.service.get_book_by_id("B999")

    self.assertIsNone(book)

  def test_create_book_and_persist(self):
    book = self.make_book()
    result = self.service.create_book(book)
    self.assertIsNotNone(result)
    assert result is not None

    self.assertEqual(result["id"], "B002")
    self.assertEqual(result["title"], "The Pragmatic Programmer")

    # Verify that the change was persisted to JSON
    saved_books = self.read_saved_books()
    self.assertIn("B002", saved_books)
    self.assertEqual(saved_books["B002"]["price"], 50.0)

  def test_create_duplicate_book(self):
    book = self.make_book(book_id="B001")
    result = self.service.create_book(book)

    self.assertIsNone(result)

    # Ensure the existing book was not overwritten
    saved_books = self.read_saved_books()
    self.assertEqual(saved_books, self.initial_books)

  def test_delete_existing_book(self):
    result = self.service.delete_book_by_id("B001")

    self.assertTrue(result)

    saved_books = self.read_saved_books()
    self.assertNotIn("B001", saved_books)

  def test_delete_nonexistent_book(self):
    result = self.service.delete_book_by_id("B999")

    self.assertFalse(result)

    # Existing data should remain unchanged
    self.assertEqual(
      self.read_saved_books(), self.initial_books
    )


if __name__ == "__main__":
  unittest.main()