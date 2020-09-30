"""
This file is intended to update the weather history.
If the file was already updated today, than we will finish.
Otherwise we will create a new file updated to today.
"""

import math
import pandas as pd
from datetime import date
from pathlib import Path
import fnmatch
import os
import numpy as np
import datetime
import API_Weather_History
import Constant
import List_Useful
from Get_Parameters_Now import find_day_in_the_week


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


def check_if_file_was_created_today(i_path_file_string):
    # Today- return TRUE, else FALSE.
    try:
        path = Path(i_path_file_string)
        timestamp = date.fromtimestamp(path.stat().st_mtime)
        if date.today() == timestamp:
            return True
        return False
    except:
        return False


def create_df_by_data_from_api(i_date_from, i_date_to):
    # input: two dates ----> output: data frame of weather history between two dates
    date_to = build_date_string(i_date_to.year, i_date_to.month, i_date_to.day)
    url_api = API_Weather_History.create_url_for_weather_data_between_two_dates(i_date_from, date_to)
    print('URL created:')
    print(url_api)
    data = API_Weather_History.request_to_api(url_api)
    df = pd.read_json(data, orient='records')

    shortDate, date_, rain, WS, temperature, humidity = [], [], [], [], [], []
    for result in df['data']:
        date_.append(result['datetime'])
        rain.append(result[U'channels'][0][u'value'])
        WS.append(result[u'channels'][3]['value'])
        temperature.append(result[u'channels'][6]['value'])
        humidity.append(result[u'channels'][7]['value'])
        shortDate.append(result['datetime'][:10])

    df.insert(2, "Short Date", shortDate, True)
    df.insert(3, "Date", date_, True)
    df.insert(4, "Rain", rain, True)
    df.insert(5, "Wind Speed", WS, True)
    df.insert(6, "Temperature", temperature, True)
    df.insert(7, "Humidity", humidity, True)

    return df


def _column_to_array(data):
    data['Rain list'] = np.tile([data['Rain'].values], (data.shape[0], 1)).tolist()
    data['Wind Speed list'] = np.tile([data['Wind Speed'].values], (data.shape[0], 1)).tolist()
    data['Temperature list'] = np.tile([data['Temperature'].values], (data.shape[0], 1)).tolist()
    data['Humidity list'] = np.tile([data['Humidity'].values], (data.shape[0], 1)).tolist()

    return data


def check_part_of_the_day_by_hours(i_hour):
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


def defining_values_of_part_of_the_day(i_document, i_start, i_end):
    rain = 0.0
    temperature = 0.0
    wind_speed = 0.0
    humidity = 0.0

    rain = sum(i_document["Rain list"][i_start:i_end + 1])
    temperature = sum(i_document["Temperature list"][i_start:i_end + 1])
    wind_speed = sum(i_document["Wind Speed list"][i_start:i_end + 1])
    humidity = sum(i_document["Humidity list"][i_start:i_end + 1])

    temperature = temperature / (i_end - i_start + 1)
    wind_speed = wind_speed / (i_end - i_start + 1)
    humidity = humidity / (i_end - i_start + 1)

    return rain, round(temperature, 1), round(wind_speed, 1), int(humidity)


def check_weather_by_values(doc, i_hour):
    res = None
    try:
        o_start, o_end = check_part_of_the_day_by_hours(i_hour)
        o_rain, o_temperature, o_wind_speed, o_humidity = defining_values_of_part_of_the_day(doc, o_start, o_end)

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
            temperature_feels_like = feels_like(o_temperature, o_wind_speed, o_humidity)

            if temperature_feels_like > Constant.HIGH_TEMPERATURES:
                # High temperatures -> 'Heat wave'
                res = List_Useful.weather[0]
            else:
                res = List_Useful.weather[1]

    except IndexError:
        return None

    return res


def feels_like(i_temperature, i_wind_speed, i_relative_humidity):
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


def create_data_frame_for_knn(weather_df):
    col = ['Short_Date', 'Part of the day', 'Day in the week', 'Weather', 'Holiday']

    df_ = pd.DataFrame(columns=col)
    ind = 0

    for i in weather_df.index:
        for j in range(len(List_Useful.hour)):
            df_.loc[ind] = np.array(
                [weather_df['Short Date'][i], List_Useful.hour[j], weather_df['Day in the Week'][i],
                 weather_df[List_Useful.hour[j]][i], weather_df['Is holiday'][i]])
            ind = ind + 1

    df_["Hour"] = np.nan

    temp_dict = dict.fromkeys(['Ticket'], 0)
    df_ = df_.assign(**temp_dict)

    df_.to_csv("knnDF", sep='\t')


o_df = None
is_file_from_scratch = False
weather_history_df = None

find_file = fnmatch.filter(os.listdir('.'), '*_weather-history')
if find_file:
    # file is exist
    file_name = find_file[0]
    date_from = find_file[0].split('_')[0]

    if date_from != str(date.today()):
        # file exist but need update
        o_df = create_df_by_data_from_api(date_from, date.today())

else:
    is_file_from_scratch = True
    # file is not exist. Initial history is from '2019/01/01'. NOTE: Pycharm fails to deal with bringing too much
    # data from API. This code works well in the Jupiter Notebook environment.
    o_df = create_df_by_data_from_api('2019/01/01', date.today())
    # o_df.to_csv('weather_history', sep='\t')

if o_df is not None:
    # new data of weather history
    df_new_data = o_df.groupby(["Short Date"]).apply(_column_to_array)
    df_new_data = df_new_data.drop_duplicates(subset='Short Date')
    df_new_data = df_new_data.drop(['Date', 'Rain', 'Wind Speed', 'Temperature', 'Humidity'], axis=1)

    df_new_data['Morning'] = df_new_data.apply(lambda row: check_weather_by_values(row, 'Morning'), axis=1)
    df_new_data['Noon'] = df_new_data.apply(lambda row: check_weather_by_values(row, 'Noon'), axis=1)
    df_new_data['Afternoon'] = df_new_data.apply(lambda row: check_weather_by_values(row, 'Afternoon'), axis=1)
    df_new_data['Evening'] = df_new_data.apply(lambda row: check_weather_by_values(row, 'Evening'), axis=1)
    df_new_data['Night'] = df_new_data.apply(lambda row: check_weather_by_values(row, 'Night'), axis=1)
    df_new_data['Day in the Week'] = df_new_data.apply(lambda row: find_day_in_the_week(row['Short Date']), axis=1)
    '''
    # -----------------------------------------------------------
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df_new_data)
    # -----------------------------------------------------------
    '''

    # Adding information for each day if is a holiday:
    holiday_israel_df = pd.read_excel("holidays_israel.xlsx")
    final_df_new_data = df_new_data.set_index(df_new_data['Short Date']).join(
        holiday_israel_df.set_index('Date')).reset_index(drop=True)
    final_df_new_data['Is holiday'] = final_df_new_data['Name'].notna()
    final_df_new_data = final_df_new_data.drop(['Name'], axis=1)
    # final_df_new_data = final_df_new_data.drop(['Name'], axis=1)

    new_file_name = build_date_string(date.today().year, date.today().month, date.today().day) + '_weather-history'
    if not is_file_from_scratch:
        weather_history_df = pd.read_csv(file_name, sep='\t')
        # rename the old file to avoid creating more file
        os.rename(file_name, new_file_name)
        weather_history_df = weather_history_df.append(final_df_new_data, ignore_index=True)
        weather_history_df = weather_history_df.drop(['Unnamed: 0'], axis=1)
        print('File is currently updated.')
        weather_history_df.to_csv(new_file_name, sep='\t')

    else:
        print('Created new file from scratch.')
        weather_history_df = final_df_new_data
        final_df_new_data.to_csv(new_file_name, sep='\t')
else:
    print('File has already been updated.')

if weather_history_df is not None:
    create_data_frame_for_knn(weather_history_df)
