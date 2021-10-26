from pymongo import MongoClient
#Providing the mongodb atlas url to connect python to mongodb using pymongo
import ssl
import json
from bson import json_util
#Use Cluster0
client = MongoClient('mongodb+srv://kpangottil:barons@cluster0.yrjds.mongodb.net/appDB?retryWrites=true&w=majority',ssl_cert_reqs=ssl.CERT_NONE)
dbname = client["appDB"]
setCollection = dbname["Hardware Sets"]
class hardwareSet():
    name: str
    capacity: int 
    availability: int
    requests: int = 0
    def __init__(self, name, capacity, availability, requests):
        self.name = name
        self.capacity = 200
        self.availability = 200
        self.requests = requests
    def create_sets(self):
        initialize_HardwareSets(self.capacity)
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
    set = {
        "Name": name,
        "Capacity": capacity,
        "Availability":capacity
    }
    setCollection.insert_one(set)
    return

def get_HWSet(name):
    hwSet = setCollection.find_one({"Name": name})
    hwSet_json = json.dumps(hwSet, indent=4, default=json_util.default)
    return hwSet_json

def checkout(name, count):
    search = {"Name": name}
    self.availability -= count
    new_availability = {"$set" : {'Availability':self.availability}}
    set = setCollection.update_one(search, new_availability)
    return

def check_in(name, count):
    search = {"Name": name}
    self.availability += count
    new_availability = {"$set" : {'Availability':self.availability}}
    set = setCollection.update_one(search, new_availability)
    return

def update_capacity(name, count):
    search = {"Name": name}
    self.availability = count
    self.capacity = count
    new_capacity = {"$set":{'Capacity': count}}
    set = setCollection.update_one(search, new_capacity)
    return
def testing_functions():
    initialize_HardwareSets(200)
    hw_set = get_HWSet("Hardware Set 1")
    print(hw_set)
    update_capacity("Hardware Set 1", 300)
    hw_set = get_HWSet("Hardware Set 1")
    print(hw_set)

client.close()
