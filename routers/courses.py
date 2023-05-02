from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.course import Course, CourseCreate
from db.setup import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from services.course import get_courses, create_course, get_course

router = APIRouter(prefix='/courses')


@router.get('/', response_model=List[Course])
async def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_courses(db, skip, limit)


@router.get('/{id}', response_model=Course)
async def read_course(id: int, db: Session = Depends(get_db)):
    db_course = get_course(db, id)
    if db_course is not None:
        return db_course
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Course)
async def create_new_course(course: CourseCreate, db: Session = Depends(get_db)):
    try:
        return create_course(db, course)
    except IntegrityError as ex:
        if ex.code == "gkpj":
            raise HTTPException(status.HTTP_400_BAD_REQUEST, ex.args)
    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "Something went wrong when creating course")
