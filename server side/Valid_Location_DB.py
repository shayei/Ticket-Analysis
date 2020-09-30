import pymongo
import Constant
from Suggest_Different_location import find_closer_valid_coordinate

# Connect to client
client = pymongo.MongoClient("********************************************")
db = client["app"]


def insert_data_mongodb(i_collection, i_coordinates):
    collection = db[i_collection]
    new_data = {}
    new_data['location'] = {}
    new_data['location']['lng'] = i_coordinates[0]
    new_data['location']['lat'] = i_coordinates[1]

    res = collection.insert_one(new_data)
    return res


def insert_new_valid_location(i_coordinates):
    res = None
    check_closet_point = find_closer_valid_coordinate("Valid_Locations", i_coordinates, Constant.TWENTY_METERS)
    if not check_closet_point:
        # There is no coordinate in the next twenty meters. Therefore we will add a new legal point to park.
        res = insert_data_mongodb("Valid_Locations", i_coordinates)

    return res


# example:
# print(insert_new_valid_location([34.778908, 32.070088]))
