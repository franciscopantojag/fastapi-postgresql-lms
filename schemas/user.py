from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class UserBase(BaseModel):
    email: str
    role: Literal[1, 2]


class UserCreate(UserBase):
    ...


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
