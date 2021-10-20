from pymongo import MongoClient
import json
from bson import json_util

# Current user model: ID, username, password, role
#TODO: add error handling for bad connections etc.

client = MongoClient(
    'mongodb+srv://aneff:barons@cluster0.yrjds.mongodb.net/appDB?retryWrites=true&w=majority')
db = client.appDB
users = db.users

class User():
    ID: str
    username: str
    password: str
    def __init__(self, ID, username, password):
        self.ID = ID
        self.username = username
        self.password = password

    def post_to_DB(self):
        post_user(self.ID, self.username, self.password)

def post_user(ID=0, username="", password=""):
    user = {"ID": ID,
            "username": username,
            "password": password}
    users.insert_one(user)
    return

def get_user_by_username(username):
    user = users.find_one({"username": username})
    user_json = json.dumps(user, indent=4, default=json_util.default)
    return user_json


def change_pass(username, new_pass):
    filter = {'username': username}
    new_pass = {"$set": {'password': new_pass}}
    user = users.update_one(filter, new_pass)
    return

def test_functions():
  post_user(3, "test", "barons", 0)
  user_json = get_user_by_username("test")
  print(user_json)
  change_pass("test", 100)
  user_json = get_user_by_username("test")
  print(user_json)