import datetime as datetime
import pymongo

import Constant
import Get_Parameters_Now
from Calculate_Percentage import str_to_int

# Connect to client
client = pymongo.MongoClient("***********************************")
db = client["app"]


#  Insert new document to collection by parameters
def insert_data_mongodb(i_collection, i_coordinates, i_date, i_hour, i_weather, i_holiday):
    collection = db[i_collection]
    new_data = {}
    new_data['location'] = {}
    new_data['location']['lng'] = i_coordinates[0]
    new_data['location']['lat'] = i_coordinates[1]

    new_data['Date'] = i_date
    new_data['Hour'] = i_hour
    new_data['Weather'] = i_weather
    new_data['Holiday'] = i_holiday

    res = collection.insert_one(new_data)
    return res


# The goal is: the client will enter as minimal details as possible
def insert_data(i_coordinates, i_date, i_time):
    """
    input: coordinates, date, hour
    output: Answer whether the operation was successful
    """
    try:
        o_relevant_collection = Get_Parameters_Now.choose_relevant_collection(i_coordinates)
        if o_relevant_collection is None:
            return "Error - Unsupported location"

        # o_relevant_collection = "test"

        time = i_time.partition(":")
        hour = int(time[0])
        minute = int(time[2])
        datetime_object = datetime.datetime.strptime(i_date, "%Y-%m-%d")
        datetime_object = datetime_object.replace(hour=hour, minute=minute)
        now = datetime.datetime.today()

        if (datetime_object - now).days < 0:
            # The report is valid in the time parameter
            if (now - datetime_object).days > 0:
                # The report is not today
                o_isHoliday = Get_Parameters_Now.check_is_holiday(i_date)
                o_hour = Get_Parameters_Now.part_of_the_day(hour)
                o_weather = Get_Parameters_Now.check_past_weather_by_date_hour(i_date, o_hour)
            else:
                # The report is today
                o_hour, o_isHoliday, o_weather, o_day_in_the_week = Get_Parameters_Now.get_relevant_parameters(hour)

            res = insert_data_mongodb(o_relevant_collection, i_coordinates, datetime_object, o_hour, o_weather,
                                      bool(o_isHoliday))
            return Constant.SUCCESS_RESPOND
        else:
            return "Error - Submitting a future report is not possible"

    except:
        return Constant.ERROR_RESPOND


# res1 = insert_data([34.7797623, 32.069129])
# print(type(res1))
# print(res1)

# res = insert_data([34.7797623, 32.069129], "2020-09-05", "9:05")
# print(res)
