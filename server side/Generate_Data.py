from datetime import datetime
from bson import json_util
import pymongo
import json
from pymongo import mongo_client
from collections import OrderedDict
import datetime as datetime
import random
from shapely.geometry import Point
import numpy as np
from datetime import datetime
from random import randrange
from datetime import timedelta
import pandas as pd
import os
import fnmatch
import List_Useful
import Area_Polygon


def open_data_frame_weather_history():
    find_file = fnmatch.filter(os.listdir('.'), '*_weather-history')
    if find_file:
        # file is exist
        file_name = find_file[0]

        df = pd.read_csv(file_name, sep='\t')
        return df
    else:
        return None


def get_weather_by_date_from_df(i_df, i_date, i_hour):
    res = i_df[i_df['Short Date'] == str(i_date)][i_hour].values[0]
    return res


def build_date_string(i_year, i_month, i_day):
    res = None
    if i_month < 10 and i_day < 10:
        res = str(i_year) + '-0' + str(i_month) + '-0' + str(i_day)
    elif i_month < 10:
        res = str(i_year) + '-0' + str(i_month) + '-' + str(i_day)
    elif i_day < 10:
        res = str(i_year) + '-' + str(i_month) + '-0' + str(i_day)
    else:
        res = str(i_year) + '-' + str(i_month) + '-' + str(i_day)

    return res


# Connect to client
client = pymongo.MongoClient("***************************************")
db = client["app"]


#  Insert new document to collection by parameters
def insert_data(i_collection, i_coordinates, i_date, i_hour, i_weather, i_holiday):
    collection = db[i_collection]
    new_data = {}
    new_data['location'] = {}
    new_data['location']['lng'] = i_coordinates.x
    new_data['location']['lat'] = i_coordinates.y

    new_data['Date'] = i_date
    new_data['Hour'] = i_hour
    new_data['Weather'] = i_weather
    new_data['Holiday'] = i_holiday

    res = collection.insert_one(new_data)


def get_random_point_in_polygon(poly):
    minx, miny, maxx, maxy = poly.bounds
    while True:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if poly.contains(p):
            return p


def range_hour(i_part_of_the_day):
    if i_part_of_the_day == List_Useful.hour[0]:
        r_hour = random.randint(7, 11)
    elif i_part_of_the_day == List_Useful.hour[1]:
        r_hour = random.randint(12, 15)
    elif i_part_of_the_day == List_Useful.hour[2]:
        r_hour = random.randint(16, 18)
    elif i_part_of_the_day == List_Useful.hour[3]:
        r_hour = random.randint(19, 23)
    else:
        r_hour = random.randint(0, 6)

    r_min = random.randint(0, 59)
    return r_hour, r_min


def random_date_within_range(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def generate_data():
    weather_history_df = open_data_frame_weather_history()
    holiday_israel_df = pd.read_excel("holidays_israel.xlsx")

    date_from = datetime.strptime('9/1/2019 1:30 PM', '%m/%d/%Y %I:%M %p')
    date_to = datetime.strptime('9/1/2020 4:50 AM', '%m/%d/%Y %I:%M %p')

    for i in range(1000):
        o_cor = get_random_point_in_polygon(Area_Polygon.Lev_Tel_Aviv)
        # Assume this division for the hour distribution of reports
        o_hour = List_Useful.hour[np.random.choice(5, 1, p=[0.3, 0.3, 0.2, 0.1, 0.1])[0]]

        o_date = random_date_within_range(date_from, date_to)
        random_hour, random_minute = range_hour(o_hour)
        o_date = o_date.replace(hour=random_hour, minute=random_minute)

        short_date = o_date.date()
        o_weather = get_weather_by_date_from_df(weather_history_df, short_date, o_hour)

        # check if holiday in dataframe
        o_isHoliday = bool((holiday_israel_df['Date'] == str(short_date)).any())

        insert_data("Reports_TA", o_cor, o_date, o_hour, o_weather, o_isHoliday)


# generate_data()
