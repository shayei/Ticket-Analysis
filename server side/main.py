import os
from datetime import datetime

import Constant
import Post_New_Data
import Calculate_Percentage
from flask import Flask, request, jsonify
import Suggest_Different_location
import Calculate_Graph_Data
import Valid_Location_DB
from Get_Parameters_Now import check_input_date

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname('D:/Program Files/untitled1/'))


@app.route('/graph', methods=['GET'])
def getGraphData():
    try:
        latitude1 = request.args.get("latitude")
        longitude1 = request.args.get("longitude")
        weather1 = request.args.get("weather")
        date1 = request.args.get("date")
        duration1 = request.args.get("duration")

        supplied_params = {"longitude": longitude1, "latitude": latitude1,
                           "weather": weather1, "day": date1, "duration": duration1}
        supplied_information = {"request_route": "/graph", "supplied_params": supplied_params}

        loc = [float(longitude1), float(latitude1)]

        res = Calculate_Graph_Data.calculate_data(loc, date1, weather1, int(duration1))

        print(res)
        received_information = {"status_code": Constant.SUCCESS_RESPOND, "calculation": res}

        return jsonify(received_information=received_information, supplied_information=supplied_information)

    except:
        received_information = {"status_code": Constant.ERROR_RESPOND, "calculation": "Error occurred"}

        return jsonify(received_information=received_information, supplied_information=supplied_information)


@app.route('/sdl', methods=['GET'])
def getSuggestTicket():
    # sdl - Suggest Different Location
    try:
        date1 = request.args.get("date")
        latitude1 = request.args.get("latitude")
        longitude1 = request.args.get("longitude")
        start_time1 = request.args.get("start_time")
        end_time1 = request.args.get("end_time")
        result_current_location1 = request.args.get("current_location_result")

        start = start_time1.replace(":", "")
        end = end_time1.replace(":", "")
        loc = [float(longitude1), float(latitude1)]
        start_num = Calculate_Percentage.str_to_int(start)
        end_num = Calculate_Percentage.str_to_int(end)
        result_current_location2 = float(result_current_location1)

        res = Suggest_Different_location.suggest_another_location(loc, start_num, end_num, result_current_location2, date1)
        print(res)

        if res is not None:

            text = "There is a " + str("{:.1f}".format(res['Result'])) + "% probability of a ticket 200 meters " + res['Direction'] + \
                   " of your location"
            percent = str("{:.1f}".format(res['Result']))
            location = {"longitude": res['Point'][0], "latitude": res['Point'][1]}
            status_code = Constant.SUCCESS_RESPOND
        else:
            text = "No area was found with a lower chance of getting a report"
            percent = None
            location = None
            status_code = "505 BAD"

        supplied_params = {"date": date1, "longitude": longitude1, "latitude": latitude1,
                           "start_time": start_time1, "end_time": end_time1,
                           "current_location_result": result_current_location1}
        supplied_information = {"request_route": "/sdl", "supplied_params": supplied_params}
        received_information = {"status_code": status_code, "text_response": text, "percent": percent,
                                "location": location}

        return jsonify(received_information=received_information, supplied_information=supplied_information)

    except:
        supplied_params = {"date": date1, "longitude": longitude1, "latitude": latitude1,
                           "start_time": start_time1, "end_time": end_time1,
                           "current_location_result": result_current_location1}
        supplied_information = {"request_route": "/sdl", "supplied_params": supplied_params}
        received_information = {"status_code": Constant.ERROR_RESPOND, "text_response": "Error occurred",
                                "percent": None, "location": None}
        return jsonify(received_information, supplied_information=supplied_information)


# example 'GET' request:
# https://e1c117c9b588.ngrok.io/gta?date="2020-09-05"&latitude=32.069129&longitude=34.7797623&start_time="0:50"&end_time="7:00"
@app.route('/gta', methods=['GET'])
def getTicket():
    # gta - Get Ticket Analysis
    try:
        date1 = request.args.get("date")
        latitude1 = request.args.get("latitude")
        longitude1 = request.args.get("longitude")
        start_time1 = request.args.get("start_time")
        end_time1 = request.args.get("end_time")

        start = start_time1.replace(":", "")
        end = end_time1.replace(":", "")
        loc = [float(longitude1), float(latitude1)]
        start_num = Calculate_Percentage.str_to_int(start)
        end_num = Calculate_Percentage.str_to_int(end)

        # If the user's input for prediction starts more than a quarter of an hour back from the current time - we
        # will return an error.
        check_input_date(date1, start_num)

        # It is assumed that a user is looking for parking in a place where it can be parked.
        # so we will keep this information about a valid parking space.
        Valid_Location_DB.insert_new_valid_location(loc)

        res = Calculate_Percentage.calculate_percentage(loc, start_num, end_num, date1)
        print(res)
        if isinstance(res, list):
            result = max(float(res[0]), Constant.MINIMUM_PERCENTAGE)
            text = "There is a " + str("{:.1f}".format(result)) + "% probability of a ticket. An inspector passed " + \
                   str(int(res[1]['Time minutes before'])) + " minutes ago " + str(res[1]['Distance']) + \
                   " meters from the current location"
            percent = str("{:.1f}".format(result))
        else:
            res = max(float(res), Constant.MINIMUM_PERCENTAGE)
            text = "There is a " + str(res) + "% probability of a ticket"
            percent = str(res)

        received_information = {"status_code": Constant.SUCCESS_RESPOND, "text_response": text, "percent": percent}
        supplied_params = {"date": date1, "longitude": longitude1, "latitude": latitude1,
                           "start_time": start_time1, "end_time": end_time1}
        supplied_information = {"request_route": "/gta", "supplied_params": supplied_params}

        return jsonify(received_information=received_information, supplied_information=supplied_information)

    except:
        supplied_params = {"date": date1, "longitude": longitude1, "latitude": latitude1,
                           "start_time": start_time1, "end_time": end_time1}
        supplied_information = {"request_route": "/gta", "supplied_params": supplied_params}

        received_information = {"status_code": Constant.ERROR_RESPOND, "text_response": "Error occurred",
                                "percent": "-1"}
        return jsonify(received_information=received_information, supplied_information=supplied_information)


@app.route('/report', methods=['POST'])
def add_plan():
    # Post: latitude, longitude, ticket_time, user_location,
    o_response = Constant.ERROR_RESPOND
    text = None
    try:

        date2 = request.json["date"]
        latitude2 = request.json["latitude"]
        longitude2 = request.json["longitude"]
        time = request.json["time"]
        # user_location_lat = request.json["user_location_lat"]
        # user_location_lng = request.json["user_location_lng"]
        supplied_params = {"date": date2, "longitude": latitude2, "latitude": longitude2, "time": time}
        supplied_information = {"request_route": "/report", "supplied_params": supplied_params}

        res = Post_New_Data.insert_data([float(longitude2), float(latitude2)], date2, time)
        if res == Constant.SUCCESS_RESPOND:
            o_response = res
        else:
            text = res
    finally:

        if o_response == Constant.SUCCESS_RESPOND:
            text = "The information was accepted by the server."

            received_information = {"status_code": Constant.SUCCESS_RESPOND, "text_response": text}
            return jsonify(received_information=received_information, supplied_information=supplied_information)
        else:
            received_information = {"status_code": Constant.ERROR_RESPOND, "text_response": "Error occurred"}

            return jsonify(received_information=received_information, supplied_information=supplied_information)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
