from typing import List
from pydantic.types import Json
from pymongo import MongoClient
import json
from bson import json_util
from .encryption import encrypt
from pydantic import BaseModel
import ssl

# Current user model: ID, username, password
#TODO: add error handling for bad connections etc.
N = 5
ENCRYPT = 1
DECRYPT = -1

client = MongoClient(
    'mongodb+srv://aneff:barons@cluster0.yrjds.mongodb.net/appDB?retryWrites=true&w=majority',  ssl_cert_reqs=ssl.CERT_NONE)
db = client.appDB
users = db.users

class User(BaseModel):
    ID: str
    username: str
    password: str

    def post_to_DB(self):
        post_user(self.ID, self.username, self.password)

# post user to DB with new ID, username, and password
def post_user(ID=0, username="", password=""):
    user = {"ID": ID,
            "username": encrypt(username, N, ENCRYPT),
            "password": encrypt(password, N, ENCRYPT)}
    users.insert_one(user)
    print(user)
    return 1

# returns error message as "message" field if no matching user
def get_user_on_login(username, password):
    encrypted_user = encrypt(username, N, ENCRYPT)
    encrypted_pass = encrypt(password, N, ENCRYPT)
    user = users.find_one({"username": encrypted_user, "password": encrypted_pass})
    # if record invalid
    if user is None:
        return({"message": "Invalid Login Info"})
    # set encrypted username back to decrypted version, same with pass
    user['username'] = username
    user['password'] = encrypt(user['password'], N, DECRYPT)
    user_json = json.dumps(user, indent=4, default=json_util.default)
    return user_json

# returns dict of ID's => usernames for all users in DB
def get_all_users():
    user_list = {}
    for each_user in users.find({}, {"_id":0, "ID":1, "username":1}):
        user_list[each_user["ID"]] = {"username": each_user["username"]}
    return user_list

# allows password change for a user by username
def change_pass(username, new_pass):
    encrypted_user = encrypt(username, N, ENCRYPT)
    encrypted_pass = encrypt(new_pass, N, ENCRYPT)
    filter = {'username': encrypted_user}
    new_pass = {"$set": {'password': encrypted_pass}}
    user = users.update_one(filter, new_pass)
    return

def test_functions():
  post_user(3, "TEST", "bcc")
  user_json = get_user_on_login("TEST", "bcc")
  print(user_json)
  change_pass("TEST", 'changedpass')
  user_json = get_user_on_login("TEST", "changedpass")
  print(user_json)
  user_json = users.find_one({"username": "VGUV"})
  print(user_json)

# test_functions()
get_all_users()