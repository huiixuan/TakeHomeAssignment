import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.routes.books import get_book_service
from backend.app.services.book_service import BookService


class TestBookRoutes(unittest.TestCase):
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

    self.test_service = BookService(self.data_file)
    app.dependency_overrides[get_book_service] = lambda: self.test_service
    self.client = TestClient(app)

  def tearDown(self):
    self.temp_dir.cleanup()

  def test_get_all_books(self):
    response = self.client.get("/api/book/")

    self.assertEqual(response.status_code, 200)
    self.assertIn("B001", response.json())

  def test_get_existing_book(self):
    response = self.client.get("/api/book/B001")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()["title"], "Clean Code")

  def test_get_nonexistent_book(self):
    response = self.client.get("/api/book/B999")

    self.assertEqual(response.status_code, 404)

  def test_add_book(self):
    payload = {
      "id": "B002",
      "title": "The Pragmatic Programmer",
      "author": "Andrew Hunt",
      "genre": "Programming",
      "price": 50.0,
    }

    response = self.client.post("/api/book/", json=payload)

    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json()["id"], "B002")

    # Verify the new book was saved
    saved_books = json.loads(self.data_file.read_text())
    self.assertIn("B002", saved_books)

  def test_add_duplicate_book(self):
      payload = {
        "id": "B001",
        "title": "Another Book",
        "author": "Jane Doe",
        "genre": "Fiction",
        "price": 20.0,
      }

      response = self.client.post("/api/book/", json=payload)

      self.assertEqual(response.status_code, 409)

  def test_add_book_with_invalid_data(self):
    payload = {
      "id": "AB",
      "title": "Clean Code",
      "author": "Robert C. Martin",
      "genre": "Programming",
      "price": 45.0,
    }

    response = self.client.post("/api/book/", json=payload)

    self.assertEqual(response.status_code, 422)

  def test_delete_existing_book(self):
    response = self.client.delete("/api/book/B001")

    self.assertEqual(response.status_code, 204)
    self.assertEqual(response.content, b"")

    saved_books = json.loads(self.data_file.read_text())
    self.assertNotIn("B001", saved_books)

  def test_delete_nonexistent_book(self):
    response = self.client.delete("/api/book/B999")

    self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()