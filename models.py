from pydantic import BaseModel
from fastapi import Query


class UserModel(BaseModel):
    user_id: int


class NewUser(BaseModel):
    id: int
    first_name: str
    last_name: str
