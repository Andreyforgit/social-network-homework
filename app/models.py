from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class UserCreate(BaseModel):
  login: str
  password: str
  first_name: str
  last_name: str
  birth_date: date
  gender: str
  interest: Optional[List[str]] = None
  city: str


class UserRead(BaseModel):
  id: int
  login: str
  first_name: str
  last_name: str
  birth_date: date
  gender: str
  interests: Optional[List[str]] = None
  city: str

class Token(BaseModel):
  access_token: str
  token_type: str = "bearer"