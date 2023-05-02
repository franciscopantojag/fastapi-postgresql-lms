from fastapi import FastAPI
from routers.users import router as user_router
from routers.courses import router as course_router
from db.setup import engine
from db.models import user, course

user.Base.metadata.create_all(bind=engine)
course.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast API LMS",
    description="LMS for managing students and courses",
    version="0.0.1",
    contact={
        "name": "Francisco Pantoja",
        "email": "franciscopantojag98@gmail.com"
    },
    license_info={
        "name": "MIT"
    }
)


app.include_router(user_router)
app.include_router(course_router)
