import Constant
import Get_Parameters_Now
import Calculate_Percentage
import datetime


def sum_data(df, i_hour_from, i_hour_to, i_day_in_the_week, i_weather, i_duration):
    param = df[(df['Day_In_The_Week'] == i_day_in_the_week) &
               (df['Weather'] == i_weather) &
               (df['Days_Before'] <= i_duration) &
               ((df['Hour_Number'] > i_hour_from) & (df['Hour_Number'] < i_hour_to)) &
               (df['Ring'] == Constant.FIRST_RING)]

    return len(param.index)


def calculate_days(row):
    days = row['Date'] - datetime.datetime.now()
    return int(abs(days.days))


def duration_two_days(i_duration):
    res = None

    if i_duration == Constant.ONE_WEEK:
        res = Constant.DAYS_ONE_WEEK
    elif i_duration == Constant.TWO_WEEKS:
        res = Constant.DAYS_TWO_WEEKS
    elif i_duration == Constant.THREE_WEEKS:
        res = Constant.DAYS_THREE_WEEKS
    elif i_duration == Constant.ONE_MONTH:
        res = Constant.DAYS_ONE_MONTH
    elif i_duration == Constant.TWO_MONTH:
        res = Constant.DAYS_TWO_MONTH
    elif i_duration == Constant.THREE_MONTH:
        res = Constant.DAYS_THREE_MONTH
    elif i_duration == Constant.HALF_YEAR:
        res = Constant.DAYS_HALF_YEAR
    else:
        res = Constant.DAYS_ONE_YEAR

    return res


def calculate_data(i_location, i_date, i_weather, i_duration):
    numbers_dict = {7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen",
                    14: "Fourteen", 15: "Fifteen", 16: "Sixteen", 17: "Seventeen", 18: "Eighteen", 19: "Nineteen",
                    20: "Twenty", 21: "Twenty_one", 22: "Twenty_two", 23: "Twenty_three"}

    relevant_collection = Get_Parameters_Now.choose_relevant_collection(i_location)

    # relevant_collection = "test"

    if relevant_collection is None:
        raise Exception('Unsupported location!')

    day_in_the_Week = Get_Parameters_Now.find_day_in_the_week(i_date)

    data_frame = Calculate_Percentage.create_relevant_data_frame(relevant_collection, i_location). \
        sort_values(by='Date')
    data_frame['Days_Before'] = data_frame.apply(lambda row: calculate_days(row), axis=1)

    o_days = duration_two_days(i_duration)
    res = {}
    for i in range(Constant.MORNING, Constant.MIDNIGHT, Constant.ONE_HOUR):
        count_data = sum_data(data_frame, i, i + Constant.ONE_HOUR,
                              day_in_the_Week, i_weather, o_days)
        print(str(count_data) + " hour: " + str(i))

        number_str = numbers_dict[int(i / 100)]
        res[number_str] = count_data

    return res


# result = calculate_data([34.780393, 32.070533], "2020-09-13", "Sunny", 52)
# print(result)
