from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import User, UserCreate
from schemas.course import Course
from db.setup import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from services.user import get_users, create_user, get_user
from services.course import get_user_courses

router = APIRouter(prefix='/users')


@router.get('/', response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip, limit)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except IntegrityError as ex:
        if ex.code == "gkpj":
            raise HTTPException(status.HTTP_400_BAD_REQUEST, ex.args)
    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "Something went wrong when creating user")


@router.get('/{id}', response_model=User)
async def read_user(id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, id)
    if db_user is not None:
        return db_user
    raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")


@router.get('/{user_id}/courses', response_model=List[Course])
async def read_user_courses(user_id: int, db: Session = Depends(get_db)):
    return get_user_courses(db, user_id)
