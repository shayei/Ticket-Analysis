import pymongo
import pprint
import json

from pymongo import mongo_client, GEO2D, GEOSPHERE

client = pymongo.MongoClient("************************************************")
db = client["app"]
# collection1 = db["Reports_TA"]
# collection1.create_index([("location", GEO2D)])


def data_by_radius_hour(i_collection, i_coordinates, i_radius_km, i_hour):
    collection = db[i_collection]
    query = {"location": {"$within": {"$center": [i_coordinates, i_radius_km / 111]}}, 'Hour': i_hour}
    return collection.find(query)


def data_by_radius_hour_holiday_warm_weather(i_collection, i_coordinates, i_radius_km, i_hour, i_holiday):
    collection = db[i_collection]
    query = {"location": {"$within": {"$center": [i_coordinates, i_radius_km / 111]}}
        , 'Hour': i_hour, 'Weather': {"$in": ['Heat wave', 'Sunny', 'Cloudy']}, 'Holiday': i_holiday}
    return collection.find(query).sort('Date')


def data_by_radius_hour_holiday_cold_weather(i_collection, i_coordinates, i_radius_km, i_hour, i_holiday):
    collection = db[i_collection]
    query = {"location": {"$within": {"$center": [i_coordinates, i_radius_km / 111]}}
        , 'Hour': i_hour, 'Weather': {"$in": ['Rainy', 'Stormy', 'Windy']}, 'Holiday': i_holiday}
    return collection.find(query).sort('Date')


def data_by_radius(i_collection, i_coordinates, i_radius_km):
    collection = db[i_collection]
    query = {"location": {"$within": {"$center": [i_coordinates, i_radius_km / 111]}}}
    return collection.find(query).sort('date', pymongo.DESCENDING)


def data_by_radius_weather_hour(i_collection, i_coordinates, i_radius_km, i_weather, i_hour):
    collection = db[i_collection]
    query = {"location": {"$within": {"$center": [i_coordinates, i_radius_km / 111]}}, 'Weather': i_weather,
             'Hour': i_hour}
    return collection.find(query)


def data_by_radius_weather(i_collection, i_coordinates, i_radius_km, i_weather):
    collection = db[i_collection]
    query = {"location": {"$within": {"$center": [i_coordinates, i_radius_km / 111]}}, 'Weather': i_weather}
    return collection.find(query)


def data_by_radius_holiday(i_collection, i_coordinates, i_radius_km, i_holiday):
    collection = db[i_collection]
    query = {"location": {"$within": {"$center": [i_coordinates, i_radius_km / 111]}}, 'Holiday': i_holiday}
    return collection.find(query)


def find_nearest_coordinate(i_collection, i_coordinates):
    collection = db[i_collection]
    query = {"location": {"$near": i_coordinates}}
    return collection.find_one(query)

# $maxDistance = your distance in Kms / 111
# query = {"location": SON([("$near", [34.7673066, 32.0328965]), ("$maxDistance", 1/111)])}

# circle (specified by center point and radius- divides by 111 for KMs):
# query1 = {"location": {"$within": {"$center": [[34.7673066, 32.0328965], 100 / 111]}}, 'Weather': 'Sunny'}

# for doc in data_by_radius("Reports_TA", [34.7673066, 32.0328965], 10):
#    pprint.pprint(doc)

# print('------------------------------------------------------')
# for doc in collection1.find(query1):
#    pprint.pprint(doc)

# query = db.collection.find({"location": {
# "$nearSphere": {"$geometry": {"type": "Point", "coordinates": [34.781929, 32.069734]}, "$maxDistance": 0.2 / 111}}})

# #for doc in collection1.find_one(qww):
# #    pprint.pprint(doc)
