import datetime
from math import sin, cos, sqrt, atan2, radians
import pandas as pd
from datetime import timedelta
import numpy as np
import List_Useful
import Read_Data_Mongodb
import Get_Parameters_Now
import Constant


def distance_two_points(i_loc_from, i_loc_to):
    lat1 = radians(i_loc_from[1])
    lon1 = radians(i_loc_from[0])

    lat2 = radians(i_loc_to[1])
    lon2 = radians(i_loc_to[0])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = Constant.EARTH_RADIUS * c

    return distance


def choose_ring(row, i_loc_from):
    # approximate radius of earth in km
    location_row = [row['location']['lng'], row['location']['lat']]
    distance = distance_two_points(i_loc_from, location_row)

    return int(distance * 10)


def str_to_int(i_str):
    num = 0
    for i in range(len(i_str)):
        if i_str[i].isdigit():
            num = num * 10 + int(i_str[i])

    return num


def create_relevant_data_frame(i_collection, i_location):
    pymongo_cursor_data = Read_Data_Mongodb.data_by_radius(i_collection, i_location,
                                                           Constant.RADIUS_THREE_HUNDRED_METERS)
    pymongo_cursor_data_df = pd.DataFrame(list(pymongo_cursor_data))

    if not pymongo_cursor_data_df.empty:
        pymongo_cursor_data_df['Short_Date'] = pymongo_cursor_data_df.apply(lambda row: row['Date'].date(), axis=1)
        pymongo_cursor_data_df['Day_In_The_Week'] = pymongo_cursor_data_df.apply(
            lambda row: row['Short_Date'].strftime("%A"), axis=1)
        pymongo_cursor_data_df['Hour_Number'] = pymongo_cursor_data_df.apply(
            lambda row: (row['Date'].hour * 100) + row['Date'].minute, axis=1)
        pymongo_cursor_data_df['Ring'] = pymongo_cursor_data_df.apply(lambda row: choose_ring(row, i_location), axis=1)
        del pymongo_cursor_data_df['_id']

    return pymongo_cursor_data_df


def sum_data_to_calculate_percentage(df, hour_from, hour_to, day=None, i_weather=None):
    o_hour, o_isHoliday, o_weather_now, o_day_in_the_week = Get_Parameters_Now.get_relevant_parameters()
    res = []

    if day:
        o_day_in_the_week = day

    if i_weather:
        o_weather_now = i_weather

    if o_weather_now in List_Useful.warm_weather:
        relevant_weather = List_Useful.warm_weather[:]
    else:
        relevant_weather = List_Useful.cold_weather[:]

    relevant_weather.remove(o_weather_now)

    for i in range(Constant.NUM_RINGS):
        param_1 = df[(df['Day_In_The_Week'] == o_day_in_the_week) &
                     (df['Weather'] == o_weather_now) &
                     ((df['Hour_Number'] > hour_from) & (df['Hour_Number'] < hour_to)) &
                     (df['Ring'] == i) &
                     (df['Holiday'] == o_isHoliday)]

        param_2 = df[(df['Day_In_The_Week'] == o_day_in_the_week) &
                     ((df['Weather'] == relevant_weather[0]) | (df['Weather'] == relevant_weather[1])) &
                     ((df['Hour_Number'] > hour_from) & (df['Hour_Number'] < hour_to)) &
                     (df['Ring'] == i) &
                     (df['Holiday'] == o_isHoliday)]

        param_3 = df[(df['Weather'] == o_weather_now) &
                     (df['Day_In_The_Week'] != o_day_in_the_week) &
                     ((df['Hour_Number'] > hour_from) & (df['Hour_Number'] < hour_to)) &
                     (df['Holiday'] == o_isHoliday) &
                     (df['Ring'] == i)]

        param_4 = df[((df['Weather'] == relevant_weather[0]) | (df['Weather'] == relevant_weather[1])) &
                     (df['Day_In_The_Week'] != o_day_in_the_week) &
                     ((df['Hour_Number'] > hour_from) & (df['Hour_Number'] < hour_to)) &
                     (df['Ring'] == i) &
                     (df['Holiday'] == o_isHoliday)]

        sum_1 = len(param_1.index)
        sum_2 = len(param_2.index)
        sum_3 = len(param_3.index)
        sum_4 = len(param_4.index)

        iter_res = [sum_1, sum_2, sum_3, sum_4]
        res.append(iter_res)

    return res


def append_results(list_1, list_2):
    res = []
    for i in range(Constant.NUM_RINGS):
        temp = []
        for j in range(Constant.NUM_PARAMS):
            temp.append(list_1[i][j] + list_2[i][j])
        res.append(temp)
    return res


def sum_data(df, i_hour_from, i_hour_to, i_weather=None):
    is_next_day = i_hour_from > i_hour_to
    if is_next_day:
        today_result = sum_data_to_calculate_percentage(df, i_hour_from, Constant.MIDNIGHT, None, i_weather)
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%A")
        next_day_result = sum_data_to_calculate_percentage(df, Constant.MIDNIGHT_ZERO, i_hour_to, tomorrow, i_weather)
        res = append_results(today_result, next_day_result)
    else:
        res = sum_data_to_calculate_percentage(df, i_hour_from, i_hour_to, None, i_weather)
    return res


def weight_data_by_importance(data_sum):
    res = []
    for i in range(Constant.NUM_RINGS):
        temp = ((data_sum[i][0] * 50) / 100) + ((data_sum[i][1] * 20) / 100) + ((data_sum[i][2] * 20) / 100) + \
               ((data_sum[i][3] * 10) / 100)
        res.append(temp)

    print(res)

    final_result = res[0] + res[1] * 0.5 + res[2] * 0.25
    if final_result > Constant.MAX_PERCENTAGE:
        final_result = Constant.MAX_PERCENTAGE

    final_result = "{:.1f}".format(final_result)
    return final_result


def calculate_ticket_weight_per_row(row, i_location):
    res = None
    now = datetime.datetime.today()
    dur = now - row['Date']

    location_last = [row['location']['lng'], row['location']['lat']]
    # distance in meters from current location to the last report
    distance = int(distance_two_points(i_location, location_last) * Constant.METERS_PER_KILOMETER)

    minutes = dur.seconds / Constant.MINUTES_IN_HOUR
    is_move_recently = Constant.RELEVANT_MINUTES_INSPECTOR_CROSSING_AREA - minutes

    # weight by distance the last report
    ticket_weight = is_move_recently * ((100 - (distance / 3)) / 100)

    if distance < Constant.HOT_SPOT_RADIUS and minutes < Constant.FIVE_MINUTES:
        ticket_weight = Constant.HOT_SPOT_PERCENTAGE

    return ticket_weight


def check_last_report_time(i_df, i_location):
    # input: database of relevant reports
    # output: check if last report was recently
    res = None

    if not i_df.empty:
        now = datetime.datetime.today()

        df_relevant_last_reports = i_df[i_df['Short_Date'] == now.date()]
        maximum_time_back = (datetime.datetime.today() - timedelta(hours=0, minutes=80)).replace(second=0, microsecond=0)
        df_relevant_last_reports = df_relevant_last_reports[df_relevant_last_reports['Date'] > maximum_time_back]
        if not df_relevant_last_reports.empty:
            df_relevant_last_reports['Influence_Report'] = df_relevant_last_reports.apply(
                lambda row: calculate_ticket_weight_per_row(row, i_location), axis=1)
            maximum_influence_last_report = df_relevant_last_reports['Influence_Report'].max()
            df_relevant_report = df_relevant_last_reports[
                df_relevant_last_reports['Influence_Report'] == maximum_influence_last_report]
            percentage_last_report = maximum_influence_last_report

            now = datetime.datetime.today()
            print(df_relevant_report.head(1)['Date'])
            print(df_relevant_report.head(1)['Date'].values[0])
            dur = now - pd.to_datetime(df_relevant_report.head(1)['Date'].values[0])

            location_last = [df_relevant_report.head(1)['location'].values[0]['lng'],
                             df_relevant_report.head(1)['location'].values[0]['lat']]
            # distance in meters from current location to the last report
            distance = int(distance_two_points(i_location, location_last) * Constant.METERS_PER_KILOMETER)

            minutes = dur.seconds / Constant.MINUTES_IN_HOUR

            res = {'Result': percentage_last_report, 'Time minutes before': minutes, 'Distance': distance}

    return res


def check_data_is_exist_at_other_days_in_the_week(i_sum_data, i_result):
    # No available data on some day but exist in others, it's a sign that the inspector is probably not on that day.
    return i_sum_data[Constant.FIRST_RING][0] + i_sum_data[Constant.FIRST_RING][1] + \
           i_sum_data[Constant.SECOND_RING][0] + i_sum_data[Constant.SECOND_RING][1] + \
           i_sum_data[Constant.THIRD_RING][0] + i_sum_data[Constant.THIRD_RING][1] == Constant.ZERO_REPORTS \
           and float(i_result)


def check_data_is_exist_in_a_different_type_of_weather(i_df, i_hour_from, i_hour_to, i_weather):
    if i_weather in List_Useful.warm_weather:
        weather_another_group = List_Useful.cold_weather[0]
    else:
        weather_another_group = List_Useful.warm_weather[0]

    o_sum_data = sum_data(i_df, i_hour_from, i_hour_to, weather_another_group)

    return o_sum_data[Constant.FIRST_RING][0] + o_sum_data[Constant.FIRST_RING][1] != Constant.ZERO_REPORTS


def is_relevant_check_last_report(i_date, i_hour):
    res = True
    input_datetime = Get_Parameters_Now.create_datetime(i_date, i_hour)
    maximum_time_back = (input_datetime - datetime.timedelta(hours=0, minutes=Constant.
                                                             RELEVANT_MINUTES_INSPECTOR_CROSSING_AREA)) \
        .replace(second=0, microsecond=0)
    time_now = datetime.datetime.today()
    print(time_now)
    print(maximum_time_back)
    if maximum_time_back > time_now:
        # The prediction is in the not-too-distant future, so it is irrelevant if an inspector has recently passed.
        res = False

    return res


def calculate_percentage(i_location, i_hour_from, i_hour_to, i_date):
    relevant_collection = Get_Parameters_Now.choose_relevant_collection(i_location)
    if relevant_collection is None:
        raise Exception('Unsupported location!')

    # relevant_collection = "test"

    one_hour_ago = i_hour_from - Constant.ONE_HOUR
    if one_hour_ago < Constant.MIDNIGHT_ZERO:
        one_hour_ago = Constant.MIDNIGHT + one_hour_ago

    one_hour_ahead = i_hour_to + Constant.ONE_HOUR
    if one_hour_ahead > Constant.MIDNIGHT:
        one_hour_ahead = one_hour_ahead - Constant.MIDNIGHT

    data_frame = create_relevant_data_frame(relevant_collection, i_location)

    if not data_frame.empty:
        data_frame = data_frame.sort_values(by='Date')

    final_result_extra = None
    if not data_frame.empty:
        res_in_range_hours = sum_data(data_frame, i_hour_from, i_hour_to)
        res_hour_ago = sum_data(data_frame, one_hour_ago, i_hour_from)
        res_hour_ahead = sum_data(data_frame, i_hour_to, one_hour_ahead)

        res_not_in_range_hours = append_results(res_hour_ago, res_hour_ahead)

        # The weight of the reports given not in the range will be lower

        weight_data_not_in_range_hours = []
        for i in range(Constant.NUM_RINGS):
            weight_data_not_in_range_hours.append(list(map(lambda num: num * 0.75, res_not_in_range_hours[i])))

        res = append_results(res_in_range_hours, list(weight_data_not_in_range_hours))
        # =====================================================================
        print(res)
        final_result = weight_data_by_importance(res)

        if check_data_is_exist_at_other_days_in_the_week(res, final_result):
            # Data is exist, but at the other days in the week
            final_result = Constant.MINIMUM_PERCENTAGE

        # We will not return zero to the user.
        # We will check what is happening in the area throughout the day

        if not float(final_result):
            res1 = sum_data(data_frame, Constant.MIDNIGHT_ZERO, Constant.MIDNIGHT)
            if res1[Constant.FIRST_RING][0] + res1[Constant.FIRST_RING][1] != Constant.ZERO_REPORTS:
                # Data is exist throughout the day, but not at the hours requested by the user
                final_result = Constant.MINIMUM_PERCENTAGE
            else:
                o_hour, o_isHoliday, o_weather_now, o_day_in_the_week = Get_Parameters_Now.get_relevant_parameters()
                if check_data_is_exist_in_a_different_type_of_weather(data_frame, one_hour_ago, one_hour_ahead,
                                                                      o_weather_now):
                    # Data is exist in a different type of weather
                    final_result = Constant.MINIMUM_PERCENTAGE
                else:
                    # no data available on the request location
                    final_result = weight_data_by_importance(res1)
                    final_result = max(float(final_result), Constant.MINIMUM_UNKNOWN_PERCENTAGE)

        final_result = min(float(final_result), Constant.MAX_PERCENTAGE)
        final_result = str(final_result)

        if is_relevant_check_last_report(i_date, i_hour_from):
            last_report = check_last_report_time(data_frame, i_location)
            if last_report is not None:
                final_result = float(final_result) + last_report['Result']
                final_result_extra = [final_result, last_report]

                if float(final_result_extra[0]) > Constant.MAX_PERCENTAGE:
                    final_result_extra[0] = Constant.MAX_PERCENTAGE

    else:
        final_result = Constant.MINIMUM_UNKNOWN_PERCENTAGE

    if final_result_extra is None:
        return str(final_result)
    else:
        return final_result_extra


# percentage = calculate_percentage([34.780439, 32.070558], 700, 705, "2020-09-23")
# print(percentage)
