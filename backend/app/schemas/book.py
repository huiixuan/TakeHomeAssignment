from pydantic import BaseModel, Field, ConfigDict

class BookCreate(BaseModel):
  model_config = ConfigDict(str_strip_whitespace=True)

  id: str = Field(min_length=4, max_length=100)
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
