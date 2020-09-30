import datetime as datetime
import fnmatch
import json
import math
import os
from datetime import timedelta

import pandas as pd
import requests
from shapely.geometry import Polygon, Point
import Area_Polygon
import Constant
import List_Useful


def check_is_holiday(i_date):
    holiday_israel_df = pd.read_excel("holidays_israel.xlsx")
    isHoliday = holiday_israel_df['Date'].astype(str).str.contains(i_date).any()

    return isHoliday


def open_data_frame_weather_history():
    find_file = fnmatch.filter(os.listdir('.'), '*_weather-history')
    if find_file:
        # file is exist
        file_name = find_file[0]

        df = pd.read_csv(file_name, sep='\t')
        return df
    else:
        return None


def check_past_weather_by_date_hour(i_date, i_hour):
    df = open_data_frame_weather_history()
    filter_df = df[df["Short Date"] == i_date]
    weather = filter_df[i_hour].values[0]
    return weather


def get_relevant_parameters(i_hour=None):
    time = datetime.datetime.now()
    if i_hour is not None:
        hour = part_of_the_day(i_hour)
    else:
        hour = part_of_the_day(time.hour)

    date_today = build_date_string_today(time.year, time.month, time.day)
    isHoliday = check_is_holiday(date_today)

    weather_now = check_weather_now(hour)
    day_in_the_week = find_day_in_the_week(date_today)

    return hour, isHoliday, weather_now, day_in_the_week


def find_day_in_the_week(i_date):
    year, month, day = (int(x) for x in i_date.split('-'))
    ans = datetime.date(year, month, day)
    return ans.strftime("%A")


def part_of_the_day(i_hour):
    res = None
    if 7 <= i_hour <= 11:
        res = List_Useful.hour[0]
    elif 12 <= i_hour <= 15:
        res = List_Useful.hour[1]
    elif 16 <= i_hour <= 18:
        res = List_Useful.hour[2]
    elif 19 <= i_hour <= 23:
        res = List_Useful.hour[3]
    else:
        res = List_Useful.hour[4]

    return res


def build_date_string_today(i_year, i_month, i_day):
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


def check_weather_now(i_part_of_the_day):
    url = "https://api.ims.gov.il/v1/envista/stations/178/data/daily"
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text.encode('utf8'))
    res = check_weather_by_values_today(data, i_part_of_the_day)

    return res


headers = {
    'Authorization': 'ApiToken *********************************'
}


def check_weather_by_values_today(doc, i_hour):
    res = None
    try:
        o_start, o_end = check_part_of_the_day_by_hours_today(i_hour)
        o_rain, o_temperature, o_wind_speed, o_humidity = defining_values_of_part_of_the_day_today(doc, o_start, o_end)

        if o_wind_speed >= Constant.STRONG_WIND_SPEED:
            # Check for high wind strength.
            # Wind without rain -> 'Windy'
            # Wind with rain -> 'Stormy'
            if o_rain > 0:
                res = List_Useful.weather[4]
            else:
                res = List_Useful.weather[5]
        elif o_rain > 0:
            # Rain without excessive wind strength -> 'Rainy'
            res = List_Useful.weather[3]
        elif o_temperature < Constant.LOW_TEMPERATURES:
            # Low temperatures -> 'Cloudy'
            res = List_Useful.weather[2]
        else:
            temperature_feels_like = feels_like_today(o_temperature, o_wind_speed, o_humidity)

            if temperature_feels_like > Constant.HIGH_TEMPERATURES:
                # High temperatures -> 'Heat wave'
                res = List_Useful.weather[0]
            else:
                res = List_Useful.weather[1]

    except IndexError:
        print('Index Error')

    return res


def check_part_of_the_day_by_hours_today(i_hour):
    i = None
    j = None

    if i_hour == List_Useful.hour[0]:
        # 7:00 - 12:00
        i = 41
        j = 70
    elif i_hour == List_Useful.hour[1]:
        # 12:00 - 16:00
        i = 71
        j = 95
    elif i_hour == List_Useful.hour[2]:
        # 16:00 - 19:00
        i = 96
        j = 113
    elif i_hour == List_Useful.hour[3]:
        # 19:00 - 24:00
        i = 114
        j = 143
    else:
        # Night
        # 00:00 - 07:00
        i = 0
        j = 40

    return i, j


def defining_values_of_part_of_the_day_today(i_document, i_start, i_end):
    rain = 0.0
    temperature = 0.0
    wind_speed = 0.0
    humidity = 0.0

    i_end = len(i_document['data']) - 1

    if i_end - i_start < 1:
        # take only the 20% last values
        i_start = int(len(i_document['data']) * 0.8)

    for k in range(i_start, i_end + 1):
        rain = rain + i_document['data'][k]['channels'][0]['value']
        temperature = temperature + i_document['data'][k]['channels'][6]['value']
        wind_speed = wind_speed + i_document['data'][k]['channels'][3]['value']
        humidity = humidity + i_document['data'][k]['channels'][7]['value']

    temperature = temperature / (i_end - i_start + 1)
    wind_speed = wind_speed / (i_end - i_start + 1)
    humidity = humidity / (i_end - i_start + 1)

    return rain, round(temperature, 1), round(wind_speed, 1), int(humidity)


def feels_like_today(i_temperature, i_wind_speed, i_relative_humidity):
    # Convert Celsius To Fahrenheit
    i_temperature = (i_temperature * 1.8) + 32
    # Convert Meters Per Second to Miles Per Hour
    i_wind_speed = i_wind_speed * 2.236936

    # Try Wind Chill first
    if i_temperature <= 50 and i_wind_speed >= 3:
        v_feels_like = 35.74 + (0.6215 * i_temperature) - 35.75 * (i_wind_speed ** 0.16) + (
                (0.4275 * i_temperature) * (i_wind_speed ** 0.16))
    else:
        v_feels_like = i_temperature

    # Replace it with the Heat Index, if necessary
    if v_feels_like == i_temperature and i_temperature >= 80:
        v_feels_like = 0.5 * (i_temperature + 61.0 + ((i_temperature - 68.0) * 1.2) + (i_relative_humidity * 0.094))

        if v_feels_like >= 80:
            v_feels_like = -42.379 + 2.04901523 * i_temperature + 10.14333127 * i_relative_humidity - .22475541 * i_temperature * i_relative_humidity - .00683783 * i_temperature * i_temperature - .05481717 * i_relative_humidity * i_relative_humidity + .00122874 * i_temperature * i_temperature * i_relative_humidity + .00085282 * i_temperature * i_relative_humidity * i_relative_humidity - .00000199 * i_temperature * i_temperature * i_relative_humidity * i_relative_humidity
            if i_relative_humidity < 13 and 80 <= i_temperature <= 112:
                v_feels_like = v_feels_like - ((13 - i_relative_humidity) / 4) * math.sqrt(
                    (17 - math.fabs(i_temperature - 95.)) / 17)
                if i_relative_humidity > 85 and 80 <= i_temperature <= 87:
                    v_feels_like = v_feels_like + ((i_relative_humidity - 85) / 10) * ((87 - i_temperature) / 5)

    feels_like_celsius = (v_feels_like - 32) / 1.8

    # print("Feels like: " + '%0.1f' % feels_like_celsius + "C")
    return feels_like_celsius


def choose_relevant_collection(i_location):
    # If an area is supported in the app we will update this function
    # input: coordinate  ----> output: relevant collection in database

    if Area_Polygon.Lev_Tel_Aviv.contains(Point(i_location)):
        return "Reports_TA"
    else:
        return None


def create_datetime(i_date, i_hour):
    res = datetime.datetime.strptime(i_date, '%Y-%m-%d')
    res = res.replace(hour=int(i_hour / 100), minute=int(i_hour % 100))
    return res


def check_input_date(i_date, i_hour):
    # If the user's input for prediction starts more than a quarter of an hour back from the current time - we
    # will return an error.
    input_datetime = create_datetime(i_date, i_hour)
    maximum_time_back = (datetime.datetime.today() - timedelta(hours=0, minutes=15)).replace(second=0, microsecond=0)
    # print(input_datetime)
    # print(maximum_time_back)
    if input_datetime < maximum_time_back:
        raise Exception('Time is irrelevant')
