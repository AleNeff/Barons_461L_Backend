# import users
from app import users
import json
from bson import json_util
from app import projects
from app import users
from app import hwSets
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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/user/login")
async def get_user_profile(username, password):
    user = users.get_user_on_login(username, password)
    return {user}

@app.get("/user/get_all")
def get_all_users():
    user_list = users.get_all_users()
    return user_list

@app.post("/user/new_user")
async def create_user(user: users.User):
    return user.post_to_DB()

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
    return projects.delete_project_by_name(request.current_user, request.project_name)

@app.post("/project/delete_id")
async def delete_project_by_id(request: projects.DeleteProjectByIdRequest):
    return projects.delete_project_by_id(request.current_user, request.project_id)

@app.post("/project/check_out")
async def check_out_hwset(request: projects.CheckOutHwsetRequest):
    return projects.check_out_hwset(
        request.current_user,
        request.project_name,
        request.hwset_name,
        request.amount_out
    )

@app.post("/project/check_in")
async def check_in_hwset(request: projects.CheckInHwsetRequest):
    return projects.check_in_hwset(
        request.current_user,
        request.project_name,
        request.hwset_name,
        request.amount_in
    )

@app.post("/project/add_user")
async def add_user(request: projects.AddUserRequest):
    return projects.add_user(
        request.current_user,
        request.project_id,
        request.user_name
    )

@app.post("/project/remove_user")
async def remove_user(request: projects.RemoveUserRequest):
    return projects.remove_user(
        request.current_user,
        request.project_id,
        request.user_name
    )

@app.get("/project/get_all")
async def get_all_projects_with_username(current_user):
    return projects.get_all_projects_with_username(current_user)

@app.get("/hwSets/get_all_hardwareSets")
async def get_all_hardwareSets():
    return hwSets.get_all_hardwareSets()

@app.get("/hwSets/get_HWSet")
async def get_hardwareSet(request: hwSets.findHWSetRequest):
    return hwSets.get_HWSET(request.hwSet_name)
