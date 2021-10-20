from pymongo import MongoClient
#Providing the mongodb atlas url to connect python to mongodb using pymongo
import ssl
#Use Cluster0
client = MongoClient('mongodb+srv://kpangottil:barons@cluster0.yrjds.mongodb.net/appDB?retryWrites=true&w=majority',ssl_cert_reqs=ssl.CERT_NONE)
dbname = client["appDB"]
newCollection = dbname["Hardware Sets"]
def add_HardwareSet(name):
    name = {
    "Capacity": "200",
    "Availability": "200",
    "Requests":"0"
    }
    newCollection.insert_one(name)
set_name = "HWSet1"
add_HardwareSet(set_name)
client.close()