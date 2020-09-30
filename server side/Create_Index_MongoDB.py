import pymongo
from pymongo import mongo_client, GEO2D, GEOSPHERE

'''
    Creating a geographic index improves the speed of searching geographic data in a database.
'''

client = pymongo.MongoClient("*******************************************")
db = client["app"]


def create_index(i_collection):
    collection1 = db[i_collection]
    collection1.create_index([("location", GEO2D)])


# example
# create_index("Reports_TA")