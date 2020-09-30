import datetime

import Calculate_Percentage
import Constant
import Get_Parameters_Now
import List_Useful


def sum_data_to_calculate_percentage(df, hour_from, hour_to, c_holiday, c_weather,
                                     c_day_in_the_week, day=None):
    res = []

    if day is not None:
        c_day_in_the_week = day

    if c_weather in List_Useful.warm_weather:
        relevant_weather = List_Useful.warm_weather[:]
    else:
        relevant_weather = List_Useful.cold_weather[:]

    relevant_weather.remove(c_weather)

    for i in range(3):
        param_1 = df[(df['Day_In_The_Week'] == c_day_in_the_week) &
                     (df['Weather'] == c_weather) &
                     ((df['Hour_Number'] > hour_from) & (df['Hour_Number'] < hour_to)) &
                     (df['Ring'] == i) &
                     (df['Holiday'] == c_holiday)]

        param_2 = df[(df['Day_In_The_Week'] == c_day_in_the_week) &
                     ((df['Weather'] == relevant_weather[0]) | (df['Weather'] == relevant_weather[1])) &
                     ((df['Hour_Number'] > hour_from) & (df['Hour_Number'] < hour_to)) &
                     (df['Ring'] == i) &
                     (df['Holiday'] == c_holiday)]

        param_3 = df[(df['Weather'] == c_weather) &
                     (df['Day_In_The_Week'] != c_day_in_the_week) &
                     ((df['Hour_Number'] > hour_from) & (df['Hour_Number'] < hour_to)) &
                     (df['Holiday'] == c_holiday) &
                     (df['Ring'] == i)]

        param_4 = df[((df['Weather'] == relevant_weather[0]) | (df['Weather'] == relevant_weather[1])) &
                     (df['Day_In_The_Week'] != c_day_in_the_week) &
                     ((df['Hour_Number'] > hour_from) & (df['Hour_Number'] < hour_to)) &
                     (df['Ring'] == i) &
                     (df['Holiday'] == c_holiday)]

        sum_1 = len(param_1.index)
        sum_2 = len(param_2.index)
        sum_3 = len(param_3.index)
        sum_4 = len(param_4.index)

        iter_res = [sum_1, sum_2, sum_3, sum_4]
        res.append(iter_res)

    return res


def append_results(list_1, list_2):
    res = []
    for i in range(3):
        temp = []
        for j in range(4):
            temp.append(list_1[i][j] + list_2[i][j])
        res.append(temp)
    return res


def sum_data(df, i_hour_from, i_hour_to, c_holiday, c_weather, c_day_in_the_week):
    is_next_day = i_hour_from > i_hour_to
    if is_next_day:
        today_result = sum_data_to_calculate_percentage(df, i_hour_from, Constant.MIDNIGHT, c_holiday, c_weather,
                                                        c_day_in_the_week)
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%A")
        next_day_result = sum_data_to_calculate_percentage(df, Constant.MIDNIGHT_ZERO, i_hour_to, c_holiday,
                                                           c_weather, c_day_in_the_week, tomorrow)
        res = append_results(today_result, next_day_result)
    else:
        res = sum_data_to_calculate_percentage(df, i_hour_from, i_hour_to, c_holiday,
                                               c_weather, c_day_in_the_week)
    return res


def check_data_is_exist_at_other_days_in_the_week(i_sum_data, i_result):
    # No available data on some day but exist in others, it's a sign that the inspector is probably not on that day.
    return i_sum_data[Constant.FIRST_RING][0] + i_sum_data[Constant.FIRST_RING][1] + \
           i_sum_data[Constant.SECOND_RING][0] + i_sum_data[Constant.SECOND_RING][1] + \
           i_sum_data[Constant.THIRD_RING][0] + i_sum_data[Constant.THIRD_RING][1] == Constant.ZERO_REPORTS \
           and float(i_result)


def check_data_is_exist_in_a_different_type_of_weather(i_df, i_hour_from, i_hour_to, i_holiday, i_weather,
                                                       i_day_in_the_week):
    if i_weather in List_Useful.warm_weather:
        weather_another_group = List_Useful.cold_weather[0]
    else:
        weather_another_group = List_Useful.warm_weather[0]

    o_sum_data = sum_data(i_df, i_hour_from, i_hour_to,
                          i_holiday, weather_another_group, i_day_in_the_week)

    return o_sum_data[Constant.FIRST_RING][0] + o_sum_data[Constant.FIRST_RING][1] != Constant.ZERO_REPORTS


def calculate_percentage(c_collection, i_location, i_hour_from, i_hour_to, c_holiday, c_weather, c_day_in_the_week):
    one_hour_ago = i_hour_from - Constant.ONE_HOUR
    if one_hour_ago < Constant.MIDNIGHT_ZERO:
        one_hour_ago = Constant.MIDNIGHT + one_hour_ago

    one_hour_ahead = i_hour_to + Constant.ONE_HOUR
    if one_hour_ahead > Constant.MIDNIGHT:
        one_hour_ahead = one_hour_ahead - Constant.MIDNIGHT

    data_frame = Calculate_Percentage.create_relevant_data_frame(c_collection, i_location)
    final_result_extra = None
    if not data_frame.empty:
        res_in_range_hours = sum_data(data_frame, i_hour_from, i_hour_to, c_holiday,
                                      c_weather, c_day_in_the_week)
        res_hour_ago = sum_data(data_frame, one_hour_ago, i_hour_from, c_holiday,
                                c_weather, c_day_in_the_week)
        res_hour_ahead = sum_data(data_frame, i_hour_to, one_hour_ahead, c_holiday,
                                  c_weather, c_day_in_the_week)

        res_not_in_range_hours = append_results(res_hour_ago, res_hour_ahead)

        # The weight of the reports given not in the range will be lower

        weight_data_not_in_range_hours = []
        for i in range(Constant.NUM_RINGS):
            weight_data_not_in_range_hours.append(list(map(lambda num: num * 0.75, res_not_in_range_hours[i])))

        res = append_results(res_in_range_hours, list(weight_data_not_in_range_hours))
        # =====================================================================
        print(res)
        final_result = Calculate_Percentage.weight_data_by_importance(res)

        if check_data_is_exist_at_other_days_in_the_week(res, final_result):
            # Data is exist, but at the other days in the week
            final_result = Constant.MINIMUM_PERCENTAGE

        # We will not return zero to the user.
        # We will check what is happening in the area throughout the day

        if not float(final_result):
            res1 = sum_data(data_frame, Constant.MIDNIGHT_ZERO, Constant.MIDNIGHT,
                            c_holiday, c_weather, c_day_in_the_week)
            if res1[Constant.FIRST_RING][0] + res1[Constant.FIRST_RING][1] != Constant.ZERO_REPORTS:
                # Data is exist throughout the day, but not at the hours requested by the user
                final_result = Constant.MINIMUM_PERCENTAGE
            else:
                if check_data_is_exist_in_a_different_type_of_weather(data_frame, one_hour_ago, one_hour_ahead,
                                                                      c_holiday, c_weather, c_day_in_the_week):
                    # Data is exist in a different type of weather
                    final_result = Constant.MINIMUM_PERCENTAGE
                else:
                    # no data available on the request location
                    final_result = Calculate_Percentage.weight_data_by_importance(res1)
                    final_result = max(float(final_result), Constant.MINIMUM_UNKNOWN_PERCENTAGE)

        final_result = min(float(final_result), Constant.MAX_PERCENTAGE)
        final_result = str(final_result)

        last_report = Calculate_Percentage.check_last_report_time(data_frame, i_location)
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


# 75% - Sunny weather
# test1 = calculate_percentage("test_weather", [34.780511, 32.070583], 800, 1000, False, 'Sunny', 'Sunday')
# print(test1)

# ---------------------------------------------------------------------------------------------------------------

# 42% - park only 20 minutes
# test2 = calculate_percentage("test_weather", [34.780511, 32.070583], 800, 820, False, 'Sunny', 'Sunday')
# print(test2)

# ---------------------------------------------------------------------------------------------------------------

# 15% - An inspector does not pass in wintry weather
# test3 = calculate_percentage("test_weather", [34.780511, 32.070583], 800, 1000, False, 'Rainy', 'Sunday')
# print(test3)

# ---------------------------------------------------------------------------------------------------------------

# 60% - Heat wave weather
# test4 = calculate_percentage("test_weather", [34.780511, 32.070583], 800, 1000, False, 'Heat wave', 'Sunday')
# print(test4)

# ---------------------------------------------------------------------------------------------------------------

# 45% - Cloudy weather
# test5 = calculate_percentage("test_weather", [34.780511, 32.070583], 800, 1000, False, 'Cloudy', 'Sunday')
# print(test5)

# ---------------------------------------------------------------------------------------------------------------

# 25% - Parking after the hours of the inspector bordering on his hours
# test6 = calculate_percentage("test_weather", [34.780511, 32.070583], 1000, 1100, False, 'Sunny', 'Sunday')
# print(test6)

# ---------------------------------------------------------------------------------------------------------------

# 15% - There is no information about the specific hours so we will check what happens the rest of the day
# test7 = calculate_percentage("test_weather", [34.780511, 32.070583], 1100, 1300, False, 'Sunny', 'Sunday')
# print(test7)

# ---------------------------------------------------------------------------------------------------------------

# 13.2%
# Third ring is 53% but first and second is 0%
# test8 = calculate_percentage("test_weather", [34.779843, 32.067806], 800, 1000, False, 'Sunny', 'Sunday')
# print(test8)

# ---------------------------------------------------------------------------------------------------------------

# 21#
# First ring 0%, second and third is 28%
# test9 = calculate_percentage("test_weather", [34.782335, 32.069122], 800, 1000, False, 'Heat wave', 'Sunday')
# print(test9)

# ---------------------------------------------------------------------------------------------------------------

# 31%
# First ring 0%, second 49%, and third is 28%
# test10 = calculate_percentage("test_weather", [34.780276, 32.068373], 800, 1000, False, 'Sunny', 'Sunday')
# print(test10)

# ---------------------------------------------------------------------------------------------------------------

# "test_day" database is path B
# An inspector usually goes through the route from Sunday to Thursday in the morning

# 82%
# test11 = calculate_percentage("test_day", [34.780511, 32.070583], 800, 1000, False, 'Sunny', "Thursday")
# print(test11)

# ---------------------------------------------------------------------------------------------------------------

# 15%
# Data is exist, but at the other days in the week
# test12 = calculate_percentage("test_day", [34.780511, 32.070583], 800, 1000, False, 'Sunny', "Friday")
# print(test12)

# ---------------------------------------------------------------------------------------------------------------

# 38%
# Weather is similar to 'Sunny'
# test13 = calculate_percentage("test_day", [34.780511, 32.070583], 800, 1000, False, 'Heat wave', "Thursday")
# print(test13)

# ---------------------------------------------------------------------------------------------------------------

# 33% - Unknown area
# test14 = calculate_percentage("test_day", [34.773898, 32.068846], 800, 1000, False, 'Heat wave', "Thursday")
# print(test14)

# ----------------------------------------------------------------------------------------------------------


# "test_graph" database is path B
# An inspector usually goes through the route on a sunny Sunday in the morning Between 8AM to 10AM
# In addition the inspector goes through the same route on a rainy Sunday in the morning Between 8AM to 10AM
# 200 tickets on a sunny weather and 250 tickets on a rainy weather

# 80%
# test15 = calculate_percentage("test_graph", [34.780271, 32.070259], 800, 1000, False, 'Sunny', "Sunday")
# print(test15)

# ----------------------------------------------------------------------------------------------------------

# 32%
# data is about similar weather- no data on heat wave
# test16 = calculate_percentage("test_graph", [34.780271, 32.070259], 800, 1000, False, 'Heat wave', "Sunday")
# print(test16)

# ----------------------------------------------------------------------------------------------------------

# Rainy : Sunday vs Monday:
# 15%
# test17 = calculate_percentage("test_graph", [34.780271, 32.070259], 800, 1000, False, 'Rainy', "Monday")
# print(test17)

# 98%
# test18 = calculate_percentage("test_graph", [34.780271, 32.070259], 800, 1000, False, 'Rainy', "Sunday")
# print(test18)


# ----------------------------------------------------------------------------------------------------------

