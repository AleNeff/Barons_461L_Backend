# import users
from app import users
import json
from bson import json_util
from app.users import User, get_user_by_username
from typing import Optional
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "https://barons461.herokuapp.com",
    "http://localhost",
    "http://localhost:8080",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/user/")
def get_user_profile(username):
    # if (username != any that we have in DB):
    #     username = "New User"
    user = get_user_by_username(username)
    return {user}

@app.post("/user/")
async def create_user(user: User):
    user.post_to_DB()
    return {"ID": user.ID, "username": user.username, "password": user.password}

# users.test_functions()