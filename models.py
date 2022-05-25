from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    id: int
