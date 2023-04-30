from typing import Optional
from fastapi import APIRouter, Path
from pydantic import BaseModel

router = APIRouter(prefix='/users')


class User(BaseModel):
    email: str
    is_active: bool
    bio: Optional[str]


users: list[User] = []


@router.get('/', response_model=list[User])
async def get_users():
    return users


@router.post('/')
async def create_user(user: User):
    users.append(user)
    return user


@router.get('/{id}')
async def get_user(id: int = Path(..., description="User Id")):
    print(type(id))
    return users[id]
