import logging
from contextlib import asynccontextmanager
from time import perf_counter
from pathlib import Path
from fastapi import FastAPI, Request
from backend.app.routes.books import router as book_router
from backend.app.services.book_service import BookService

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "books.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("backend")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the JSON file once when the application starts
    app.state.book_service = BookService(DATA_FILE)
    logger.info("Loaded book data from %s", DATA_FILE)
    yield
    logger.info("Application shutting down")


app = FastAPI(
    title="Book API",
    description="A CRUD API backed by a JSON file.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = perf_counter()
    try:
      response = await call_next(request)
      elapsed = perf_counter() - start
      logger.info(
        "%s %s -> %s (%.3fs)",
        request.method,
        request.url.path,
        response.status_code,
        elapsed,
      )
      return response
    except Exception:
      logger.exception("Request failed: %s %s", request.method, request.url.path)
      raise

app.include_router(book_router)

@app.get("/health", tags=["health"])
def health_check():
  return {"status": "ok"}
