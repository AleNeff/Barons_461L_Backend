from pymongo import MongoClient
#Providing the mongodb atlas url to connect python to mongodb using pymongo
import ssl
from pydantic import BaseModel
import json
from bson import json_util
from pymongo.errors import DuplicateKeyError
#Use Cluster0
client = MongoClient('mongodb+srv://kpangottil:barons@cluster0.yrjds.mongodb.net/appDB?retryWrites=true&w=majority',ssl_cert_reqs=ssl.CERT_NONE)
dbname = client["appDB"]
setCollection = dbname["Hardware Sets"]

class HWSet(BaseModel):
    Name: str
    Capacity: int
    Availability: int
    def add_HardwareSet(self):
        return add_HardwareSets(self.Name, self.Capacity)

def initialize_HardwareSets(capacity):
    HWSet1 = {
    "Name": "Hardware Set 1",
    "Capacity": capacity,
    "Availability": capacity,
    }
    HWSet2 = {
    "Name": "Hardware Set 2",
    "Capacity": capacity,
    "Availability": capacity,
    }
    setCollection.insert_one(HWSet1)
    setCollection.insert_one(HWSet2)
    return

def add_HardwareSets(name="", capacity=0):
    #Creates a new hardware set and adds it to the database, if a duplicate exists it is not added
    set = {
        "Name": name,
        "Capacity": capacity,
        "Availability":capacity
    }
    if setCollection.find_one({"Name":name}) is not None:
        return -1
    else:
        setCollection.insert_one(set)
        return 0

def remove_HWSet(name):
    if setCollection.find_one({"Name":name}) is not None:
        hwSet = setCollection.find_one({"Name": name})
        setCollection.delete_one(hwSet)
       

def get_HWSet(name):
    if setCollection.find_one({"Name":name}) is not None:
            hwSet = setCollection.find_one({"Name": name})
            hwSet_json = json.dumps(hwSet, indent=4, default=json_util.default)
            return hwSet_json

#returns all hardware sets

def get_all_hardwareSets():
    hwset_list = setCollection.find()
    result = []
    for each_set in hwset_list:
        set = HWSet(**each_set)
        result.append(set)
    return result

def update_capacity(name, count):
    if setCollection.find_one({"Name":name}) is not None:
        search = setCollection.find_one({"Name":name})
        new_capacity = {"$set":{'Capacity': count}}
        setCollection.update_one(search, new_capacity)
        new_availability = {"$set" : {'Availability':count}}
        search = setCollection.find_one({"Name":name})
        setCollection.update_one(search, new_availability)
    return

def testing_functions():
    #initialize_HardwareSets(200)
    #hw_set = get_HWSet("Hardware Set 1")
    #print(hw_set)
    #update_capacity("Hardware Set 1", 300)
    #hw_set = get_HWSet("Hardware Set 2")
    add_HardwareSets("Hardware Set Test", 300)
    #remove_HWSet("string")
    #out = remove_HWset("Test")
   # print(out)
    #print(hw_set)
    print(get_all_hardwareSets())
#testing_functions()
client.close()

