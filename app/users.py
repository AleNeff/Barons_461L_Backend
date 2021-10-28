from pymongo import MongoClient
import json
from bson import json_util
from .encryption import encrypt
from pydantic import BaseModel

# Current user model: ID, username, password
#TODO: add error handling for bad connections etc.
N = 5
ENCRYPT = 1
DECRYPT = -1

client = MongoClient(
    'mongodb+srv://aneff:barons@cluster0.yrjds.mongodb.net/appDB?retryWrites=true&w=majority')
db = client.appDB
users = db.users

class User(BaseModel):
    ID: str
    username: str
    password: str

    def post_to_DB(self):
        post_user(self.ID, self.username, self.password)

def post_user(ID=0, username="", password=""):
    user = {"ID": ID,
            "username": encrypt(username, N, ENCRYPT),
            "password": encrypt(password, N, ENCRYPT)}
    users.insert_one(user)
    print(user)
    return

def get_user_by_username(username):
    encrypted_user = encrypt(username, N, ENCRYPT)
    user = users.find_one({"username": encrypted_user})
    # set encrypted username back to decrypted version, same with pass
    user['username'] = username
    user['password'] = encrypt(user['password'], N, DECRYPT)
    user_json = json.dumps(user, indent=4, default=json_util.default)
    return user_json


def change_pass(username, new_pass):
    encrypted_user = encrypt(username, N, ENCRYPT)
    encrypted_pass = encrypt(new_pass, N, ENCRYPT)
    filter = {'username': encrypted_user}
    new_pass = {"$set": {'password': encrypted_pass}}
    user = users.update_one(filter, new_pass)
    return

def test_functions():
  post_user(3, "TEST", "bcc")
  user_json = get_user_by_username("TEST")
  print(user_json)
  change_pass("TEST", 'changedpass')
  user_json = get_user_by_username("TEST")
  print(user_json)
  user_json = users.find_one({"username": "VGUV"})
  print(user_json)

# test_functions()