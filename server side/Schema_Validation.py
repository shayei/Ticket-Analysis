# Add a new collection with document restrictions
import pymongo
from pymongo import mongo_client
from collections import OrderedDict

# Connect to client
client = pymongo.MongoClient("************************************************")
db = client["app"]

nameNewCollection = "Reports_TA"
db.create_collection(nameNewCollection)  # Force create!

#  $jsonSchema expression type is preferred.  New since v3.6 (2017):

vexpr = {"$jsonSchema":
    {
        "bsonType": "object",
        "required": ["location", "Date", "Hour", "Weather", "Holiday"],
        "properties": {
            "location": {
                        "bsonType": "object",
                        "required": ["lng", "lat"],
                        "properties": {
                            "lng": {
                                "bsonType": "double",
                                "minimum": -180,
                                "maximum": 180
                            },
                            "lat": {
                                "bsonType": "double",
                                "minimum": -90,
                                "maximum": 90
                            }
                        },
                    },
            "Date": {
                # Date of the actual report
                "bsonType": "date",
                "description": "must be a date and is required"
            },
            "Hour": {
                "enum": ["Morning", "Noon", "Afternoon", "Evening", "Night", None],
                "description": "can only be one of the enum values and is required"
            },
            "Weather": {
                "enum": ["Heat wave", "Sunny", "Cloudy", "Rainy", "Stormy", "Windy", None],
                "description": "can only be one of the enum values and is required"
            },
            "Holiday": {
                "bsonType": "bool",
                "description": "must be a boolean and is required"
            },

        }
    }
}

cmd = OrderedDict([('collMod', nameNewCollection),
                   ('validator', vexpr),
                   ('validationLevel', 'moderate')])

db.command(cmd)
