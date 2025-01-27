from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

fake_database = []


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Hello, World!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(fake_database) + 1, **user.model_dump())
    fake_database.append(user_with_id)
    return user_with_id


@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {"users": fake_database}
