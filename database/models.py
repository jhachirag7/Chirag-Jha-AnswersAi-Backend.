from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None




class Questions(BaseModel):
    title: str