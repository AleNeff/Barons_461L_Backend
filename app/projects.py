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

    # def __init__(self, name, description, id, owner):
    #     """Constructor for project creation."""
    #     self.project_name = name
    #     self.project_description = description
    #     self.project_id = id
    #     self.project_owner = owner
    #     self.users_list = [owner]
    #     self.checked_out = {}

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

def delete_project_by_name(name):
    """Delete a project by project name (str)"""
    PROJECTS_COLLECTION.delete_one({"project_name": name})

def delete_project_by_id(id):
    """Delete a project by project id (str)"""
    PROJECTS_COLLECTION.delete_one({"project_id": id})

def check_out_hwset(project_name, hwset_name, amount_out):
    """
    Check out hwset_amount (int) units of hardware from hwset_name (str) to project_name (str)

    Returns 0 for success or -1 for failure (insufficient availability / funds)
    """
    #use hwSets.py code udpate Hardware Sets collection
    #TODO: return -1 for failure
    
    project_dict = PROJECTS_COLLECTION.find_one({"project_name": project_name})
    project = Project()
    project.dict_to_class(project_dict)

    if hwset_name not in project.checked_out.keys():
        project.checked_out[hwset_name] = amount_out #TODO: depends on availability
    else:
        project.checked_out[hwset_name] += amount_out #TODO: depends on availability

    PROJECTS_COLLECTION.find_one_and_update(
        {"project_name": project_name}, 
        {"$set": {"checked_out": project.checked_out}})

    #TODO: return 0 for success

def check_in_hwset(project_name, hwset_name, amount_in):
    """
    Check in hwset_amount (int) units of hardware to hwset_name (str) from project_name (str)

    Returns 0 for success or -1 for failure (checking in more than amount checked out)
    """
    #TODO: use hwSets.py code udpate Hardware Sets collection
    #TODO: return -1 for failure
    
    project_dict = PROJECTS_COLLECTION.find_one({"project_name": project_name})
    project = Project()
    project.dict_to_class(project_dict)

    project.checked_out[hwset_name] -= amount_in #TODO: depends on availability

    PROJECTS_COLLECTION.find_one_and_update(
        {"project_name": project_name}, 
        {"$set": {"checked_out": project.checked_out}})

    #TODO: return 0 for success

def add_user(project_name, user_name):
    """
    Add user with user_name (str) into project_name (str)
    """
    project_dict = PROJECTS_COLLECTION.find_one({"project_name": project_name})
    project = Project()
    project.dict_to_class(project_dict)

    if user_name not in project.users_list:
        project.users_list.append(user_name)

    PROJECTS_COLLECTION.find_one_and_update(
        {"project_name": project_name}, 
        {"$set": {"users_list": project.users_list}})

def remove_user(project_name, user_name):
    """
    Remove user with user_name (str) from project_name (str)
    """
    project_dict = PROJECTS_COLLECTION.find_one({"project_name": project_name})
    project = Project()
    project.dict_to_class(project_dict)

    try:
        project.users_list.remove(user_name)
    except ValueError:
        return

    PROJECTS_COLLECTION.find_one_and_update(
        {"project_name": project_name}, 
        {"$set": {"users_list": project.users_list}})

def get_all_projects_with_username(user_name):
    """
    Get all projects from MongoDB with username user_name (str)
    """
    all_project_list = PROJECTS_COLLECTION.find()
    result = []
    for potential_project in all_project_list:
        project = Project(**potential_project)
        if user_name in project.users_list:
            result.append(project)
    return result



# print(create_project("Project 5", "Description 0", "0005", "barons@gmail.com"))
# delete_project_by_name("Project 5")
# check_out_hwset("Project 4", "HWSet2", 10)
# check_in_hwset("Project 4", "HWSet2", 10)
# add_user("Project 4", "nghi@gmail.com")
# remove_user("Project 4", "nghi@gmail.com")
# get_all_projects_with_username("nghi@gmail.com")

