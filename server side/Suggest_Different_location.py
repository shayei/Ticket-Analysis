import pandas as pd
from pygc import great_circle
import Calculate_Percentage
import time

import Constant
import Read_Data_Mongodb
from Get_Parameters_Now import choose_relevant_collection
import List_Useful


def find_closer_valid_coordinate(i_collection, i_location, i_maximum_distance):
    result = None

    nearest_object = Read_Data_Mongodb.find_nearest_coordinate(i_collection, i_location)
    if nearest_object:
        nearest_object_coordinates = [nearest_object['location']['lng'], nearest_object['location']['lat']]
        distance_closer_point = int(Calculate_Percentage.distance_two_points(i_location, nearest_object_coordinates) * \
                                    Constant.METERS_PER_KILOMETER)
        # print("distance" + str(distance_closer_point))
        if distance_closer_point < i_maximum_distance:
            result = [nearest_object_coordinates, distance_closer_point]

    return result


def suggest_another_location(i_location, i_hour_from, i_hour_to, i_result_current_location, i_date):
    distance_meters = Constant.DISTANCE_FROM_CURRENT_LOCATION
    collect_res = []

    # for testing- No suggestion found!
    # i_result_current_location = 1

    for key, value in List_Useful.azimuth_direction.items():
        get_location = great_circle(distance=distance_meters, azimuth=value, latitude=i_location[1],
                                    longitude=i_location[0])
        new_location = [get_location['longitude'], get_location['latitude']]
        relevant_collection = choose_relevant_collection(new_location)
        if relevant_collection is not None:

            # relevant_collection = 'test'

            valid_location_report_DB = find_closer_valid_coordinate(relevant_collection, new_location,
                                                                    Constant.CLOSE_AREA)
            valid_location_DB = find_closer_valid_coordinate(Constant.VALID_LOCATIONS_DATA_BASE, new_location, Constant.CLOSE_AREA)
            if valid_location_report_DB and valid_location_DB:
                # Take closet point
                if valid_location_report_DB[1] < valid_location_DB[1]:
                    valid_location = valid_location_report_DB
                else:
                    valid_location = valid_location_DB
            else:
                # At least one result is 'None'
                valid_location = valid_location_DB or valid_location_report_DB

            print(new_location, valid_location)

            if valid_location:
                res = Calculate_Percentage.calculate_percentage(valid_location[0], i_hour_from, i_hour_to, i_date)

                if isinstance(res, list):
                    collect_res.append({"Direction": key, "Point": valid_location[0], "Result": float(res[0])})
                else:
                    collect_res.append({"Direction": key, "Point": valid_location[0], "Result": float(res)})

    minimum_value = None
    print(collect_res)
    if collect_res:
        minimum_value = min(collect_res, key=lambda x: x['Result'])
        if minimum_value['Result'] < Constant.MINIMUM_PERCENTAGE:
            minimum_value['Result'] = Constant.MINIMUM_PERCENTAGE

        if i_result_current_location <= minimum_value['Result']:
            minimum_value = None

    return minimum_value


# start = time.time()
# run = suggest_another_location([34.774393, 32.061752], 800, 1000, 5)
# print("There is a " + str(run['Result']) + "% probability of a ticket " + run['Direction'] + \
#       " of your location. Coordinates: " + str(run['Point']))
# end = time.time()
#
# print(run)
# print("Time action: {:.1f} seconds.".format(end - start))
