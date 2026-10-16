from typing import TypedDict
from pydantic import BaseModel, Field, ConfigDict

class BookData(TypedDict):
  title: str
  author: str
  genre: str
  price: float

class BookResponseData(BookData):
  id: str

class BookCreate(BaseModel):
  model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

  id: str = Field(min_length=4, max_length=100, pattern=r"^B")
  title: str = Field(min_length=1, max_length=100)
  author: str = Field(min_length=1, max_length=100)
  genre: str = Field(min_length=1, max_length=100)
  price: float = Field(ge=1, allow_inf_nan=False)

class BookResponse(BaseModel):
  id: str
  title: str
  author: str
  genre: str
  price: float
