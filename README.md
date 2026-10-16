# Book API

A RESTful API built with **FastAPI** and Python for managing a collection of books. The application uses a JSON file for persistent storage and is containerised with Docker and deployed on Render.

## Live Demo

- **API Base URL:** `https://takehomeassignment-24wg.onrender.com`
- **Interactive API Documentation:** `https://takehomeassignment-24wg.onrender.com/docs`

## Features

- **CRUD operations:** Retrieve all books, retrieve a book by ID, add new books, and delete books.
- **Request validation:** Pydantic validates incoming data, including book ID format, required fields, field lengths, and price constraints.
- **Error handling:** Returns appropriate HTTP status codes for invalid requests, missing books, and duplicate IDs.
- **Request logging:** Middleware logs incoming requests, HTTP methods, paths, response status codes, and request durations.
- **Dependency injection:** FastAPI's `Depends` injects the book service into route handlers, making the application easier to test and maintain.
- **JSON persistence:** Book data is loaded into memory at application startup and saved to the JSON file when books are added or deleted.
- **Automated tests:** Unit tests cover service logic and API endpoints.
- **Docker support:** A Dockerfile packages the application and its dependencies for deployment.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- JSON file storage
- Docker
- Render
- `unittest` and FastAPI `TestClient`

## API Endpoints

| Method | Endpoint | Success Status | Description |
|---|---|---|---|
| `GET` | `/api/book/` | `200 OK` | Retrieve all books |
| `GET` | `/api/book/{id}` | `200 OK` | Retrieve a book by ID |
| `POST` | `/api/book/` | `201 Created` | Add a new book |
| `DELETE` | `/api/book/{id}` | `204 No Content` | Delete a book by ID |
| `GET` | `/health` | `200 OK` | Check application health |

### Validation Rules

- Book IDs must start with uppercase `B` and contain between 4 and 100 characters.
- Titles, authors, and genres must contain between 1 and 100 characters after whitespace trimming.
- Prices must be finite numbers greater than or equal to `1`.
- Unexpected fields in a book creation request are rejected.

### Error Responses

| Status | Meaning |
|---|---|
| `404 Not Found` | The requested book does not exist |
| `409 Conflict` | A book with the submitted ID already exists |
| `422 Unprocessable Entity` | Request data or book ID fails validation |

## Example Request

Create a book using `POST /api/book/`:

```json
{
  "id": "B003",
  "title": "Designing Data-Intensive Applications",
  "author": "Martin Kleppmann",
  "genre": "Software Engineering",
  "price": 60.0
}
```

Example successful response (`201 Created`):

```json
{
  "id": "B003",
  "title": "Designing Data-Intensive Applications",
  "author": "Martin Kleppmann",
  "genre": "Software Engineering",
  "price": 60.0
}
```

## Project Structure

```text
.
├── backend/
│   └── app/
│       ├── data/
│       │   └── books.json
│       ├── routes/
│       │   └── book.py
│       ├── schemas/
│       │   └── book.py
│       ├── services/
│       │   └── book_service.py
│       └── main.py
├── tests/
│   ├── test_book_routes.py
│   └── test_book_service.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting Started Locally

### Prerequisites

- Python 3.11 or later
- pip

### Installation

Clone the repository and navigate to the project root:

```bash
git clone <your-repository-url>
cd <your-repository-directory>
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Open `http://127.0.0.1:8000/docs` to explore and test the endpoints using Swagger UI.

## Running with Docker

Build the Docker image from the project root:

```bash
docker build -t book-api .
```

Run the container:

```bash
docker run --rm -p 8000:8000 book-api
```

The API will be available at `http://localhost:8000`.

## Running Tests

Run the test suite from the project root:

```bash
python -m unittest discover -s backend/tests -v
```

The tests cover book retrieval, creation, duplicate ID handling, invalid input, deletion, missing resources, and persistence of changes.

## Deployment

The Book API is deployed on **Render** and can be accessed through the hosted service URL.

- **API Base URL:** `https://takehomeassignment-24wg.onrender.com`
- **Interactive API Documentation:** `https://takehomeassignment-24wg.onrender.com/docs`
- **Health Check:** `https://takehomeassignment-24wg.onrender.com/health`

The interactive API documentation allows users to explore the available endpoints, submit requests, and view responses directly in their browser without setting up a local environment.

**Data Persistence:** Book records are stored in a JSON file on the server's local filesystem. As the application is deployed on Render's free instance without a persistent disk, changes to book records may be lost when the service restarts, redeploys, or spins down. The initial book data is restored when the application loads the JSON file included in the deployed code.

## Design Notes

The application separates responsibilities into three layers:

- **Routes:** Handle HTTP requests, response status codes, and error handling.
- **Schemas:** Define request validation rules and response structures.
- **Services:** Contain business logic and manage in-memory book data and JSON persistence.

The JSON file is loaded at application startup to avoid repeatedly reading the file for every request. A lock protects concurrent operations within a single process.
