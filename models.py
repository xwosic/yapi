from pydantic import BaseModel
from fastapi import Query


class UserId(BaseModel):
    user_id: int


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
