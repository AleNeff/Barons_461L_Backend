# import users
from app import users
import json
from bson import json_util
from app import projects
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

@app.post("/project/create")
async def create_project(request: projects.CreateProjectRequest):
    return projects.create_project(
        request.project_name, 
        request.project_description, 
        request.project_id, 
        request.project_owner
    )

@app.post("/project/delete_name")
async def delete_project_by_name(request: projects.DeleteProjectByNameRequest):
    projects.delete_project_by_name(request.user, request.project_name)

@app.post("/project/delete_id")
async def delete_project_by_id(request: projects.DeleteProjectByIdRequest):
    projects.delete_project_by_id(request.user, request.project_id)

@app.post("/project/check_out")
async def check_out_hwset(request: projects.CheckOutHwsetRequest):
    return projects.check_out_hwset(
        request.user,
        request.project_name,
        request.hwset_name,
        request.amount_out
    )

@app.post("/project/check_in")
async def check_in_hwset(request: projects.CheckInHwsetRequest):
    return projects.check_in_hwset(
        request.user,
        request.project_name,
        request.hwset_name,
        request.amount_in
    )

@app.post("/project/add_user")
async def add_user(request: projects.AddUserRequest):
    return projects.add_user(
        request.user,
        request.project_name,
        request.user_name
    )

@app.post("/project/remove_user")
async def remove_user(request: projects.RemoveUserRequest):
    return projects.remove_user(
        request.user,
        request.project_name,
        request.user_name
    )

@app.get("/project/get_all")
async def remove_user(request: projects.GetAllProjectWithUserNameRequest):
    return projects.get_all_projects_with_username(request.user)

# users.test_functions()