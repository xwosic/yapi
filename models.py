from pydantic import BaseModel
from fastapi import Query


class UserModel(BaseModel):
    user_id: int
    username: str = Query(None)
