import json
import requests

# examples:
# url = "https://api.ims.gov.il/v1/envista/stations/178/data/daily/2019/01/15"
# url = "https://api.ims.gov.il/v1/envista/stations/178/data?from=2020/01/18&to=2020/01/20"

headers = {
    'Authorization': 'ApiToken *******************************'
}


def create_url_for_weather_data_one_day(i_date):
    # string in format: YYYY/MM/DD
    # 178 station of Tel-Aviv
    res = "https://api.ims.gov.il/v1/envista/stations/178/data/daily/" + i_date
    return res


def create_url_for_weather_data_between_two_dates(i_string_from, i_string_to):
    # each string in format: YYYY/MM/DD
    # 178 station of Tel-Aviv
    res = "https://api.ims.gov.il/v1/envista/stations/178/data?from=" + i_string_from + "&to=" + i_string_to
    return res


def request_to_api(i_url):
    response = requests.request("GET", i_url, headers=headers)
    data = response.text
    return data


