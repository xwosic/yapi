from pydantic import BaseModel
from typing import Optional


class UserId(BaseModel):
    user_id: int


class User(BaseModel):
    id: int
    first_name: str
    last_name: str


class FilterUser(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
