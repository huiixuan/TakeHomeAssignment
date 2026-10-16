from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import books

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
  allow_credentials=True
)

app.include_router(books.router)