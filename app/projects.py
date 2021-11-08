from enum import unique
from typing import Dict, List
from pymongo import MongoClient
from pydantic import BaseModel

from pymongo.errors import DuplicateKeyError

#Constants for cluster, database, and collections
CLIENT = MongoClient("mongodb+srv://nnguyen:barons@cluster0.yrjds.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
DATABASE = CLIENT["appDB"]
PROJECTS_COLLECTION = DATABASE["projects"]
HWSETS_COLLECTION = DATABASE["Hardware Sets"]

class Project(BaseModel):

    #Private project attributes
    project_name: str = ""
    project_description: str = ""
    project_id: str = ""
    project_owner: str = ""
    users_list: List[str] = []
    checked_out: Dict[str, str] = {}

    def dict_to_class(self, dict):
        for key in dict:
            if key != "_id":
                setattr(self, key, dict[key])

def create_project(name, description, id, owner):
    """
    Creates a new project and adds it to database.

    Returns 0 for success or -1 for failure (duplicate project name or ID)
    """
    project = {
        "project_name": name,
        "project_description": description,
        "project_id": id,
        "project_owner": owner,
        "users_list": [owner],
        "checked_out": {}
    }

    try:
        PROJECTS_COLLECTION.insert_one(project)
        return 0
    except DuplicateKeyError as e:
        return -1

def delete_project_by_name(current_user, name):
    """Delete a project by project name (str)"""
    PROJECTS_COLLECTION.delete_one({"project_name": name})

def delete_project_by_id(current_user, id):
    """Delete a project by project id (str)"""
    PROJECTS_COLLECTION.delete_one({"project_id": id})

def check_out_hwset(current_user, project_name, hwset_name, amount_out):
    """
    Check out amount_out (int) units of hardware from hwset_name (str) to project_name (str)

    Returns 0 for success, 1 limited checkout (insufficient availability), -1 for invalid input
    """
    result = -1
    availability = HWSETS_COLLECTION.find_one({"Name": "string"})["Availability"]

    if amount_out < 0: 
        return result 
    elif amount_out > availability:
        amount_out = availability
        result = 1
    else:
        result = 0

    HWSETS_COLLECTION.find_one_and_update(
        {"Name": hwset_name}, 
        {"$inc": {"Availability": -amount_out}}
    )
    
    project_dict = PROJECTS_COLLECTION.find_one({"project_name": project_name})
    project = Project()
    project.dict_to_class(project_dict)

    if hwset_name not in project.checked_out.keys():
        project.checked_out[hwset_name] = amount_out 
    else:
        project.checked_out[hwset_name] += amount_out 

    PROJECTS_COLLECTION.find_one_and_update(
        {"project_name": project_name}, 
        {"$set": {"checked_out": project.checked_out}}
    )

    return result

def check_in_hwset(current_user, project_name, hwset_name, amount_in):
    """
    Check in amount_in (int) units of hardware to hwset_name (str) from project_name (str)

    Returns 0 for success, 1 for checking in more than amount checked out, -1 for invalid input
    """
    project_dict = PROJECTS_COLLECTION.find_one({"project_name": project_name})
    project = Project()
    project.dict_to_class(project_dict)

    if amount_in < 0:
        return -1
    elif amount_in > project.checked_out[hwset_name]:
        return 1
        
    project.checked_out[hwset_name] -= amount_in 

    PROJECTS_COLLECTION.find_one_and_update(
        {"project_name": project_name}, 
        {"$set": {"checked_out": project.checked_out}}
    )

    HWSETS_COLLECTION.find_one_and_update(
        {"Name": hwset_name}, 
        {"$inc": {"Availability": amount_in}}
    )

    return 0

def add_user(current_user, project_id, user_name):
    """
    Add user with user_name (str) into project with ID project_id (str)
    """
    project_dict = PROJECTS_COLLECTION.find_one({"project_id": project_id})
    project = Project()
    project.dict_to_class(project_dict)

    if user_name not in project.users_list:
        project.users_list.append(user_name)

    PROJECTS_COLLECTION.find_one_and_update(
        {"project_id": project_id}, 
        {"$set": {"users_list": project.users_list}}
    )

def remove_user(current_user, project_id, user_name):
    """
    Remove user with user_name (str) from project with ID project_id (str)
    """
    project_dict = PROJECTS_COLLECTION.find_one({"project_id": project_id})
    project = Project()
    project.dict_to_class(project_dict)

    try:
        project.users_list.remove(user_name)
    except ValueError:
        return

    PROJECTS_COLLECTION.find_one_and_update(
        {"project_id": project_id}, 
        {"$set": {"users_list": project.users_list}}
    )

def get_all_projects_with_username(current_user):
    """
    Get all projects from MongoDB with username user (str)
    """
    all_project_list = PROJECTS_COLLECTION.find()
    result = []
    for potential_project in all_project_list:
        project = Project(**potential_project)
        if current_user in project.users_list:
            result.append(project)
    return result

# # # # # # # Request Body Models for FastAPI # # # # # # #

class CreateProjectRequest(BaseModel):
    project_name: str
    project_description: str
    project_id: str
    project_owner: str

class DeleteProjectByNameRequest(BaseModel):
    current_user: str
    project_name: str

class DeleteProjectByIdRequest(BaseModel):
    current_user: str
    project_id: str

class CheckOutHwsetRequest(BaseModel):
    current_user: str
    project_name: str
    hwset_name: str
    amount_out: int

class CheckInHwsetRequest(BaseModel):
    current_user: str
    project_name: str
    hwset_name: str
    amount_in: int

class AddUserRequest(BaseModel):
    current_user: str
    project_id: str
    user_name: str

class RemoveUserRequest(BaseModel):
    current_user: str
    project_id: str
    user_name: str
