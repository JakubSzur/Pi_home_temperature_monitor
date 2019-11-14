import urllib.request
import json
from datetime import datetime

# class to collect wheather values
class Weather:

    def __init__(self, time, temperature, pressure, humidity, description,
                 rain=None, snow=None):
        self.time = time
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.description = description
        if rain is None:
            self.rain = "No rain"
        if snow is None:
            self.snow = "No snow"


# function to get JSON with weather forecast
def get_json():
    # get API key from file to connect with API
    with open('APPID.txt') as file:
        api_key = file.readline()
    # get json with hourly forecast from Openwheather API
    with urllib.request.urlopen('http://api.openweathermap.org//data//2.5/'
                                f'forecast/?id=7531890&APPID={api_key}'
                                '&units=metric') as url:
        data = json.loads(url.read().decode())
    return data


# get specific values from JSON and put them into list
def parse_data(json_file):
    # list to collect objects with values
    weather_values = []
    # get forecast values from JSON file
    for element in json_file['list']:
        # get time
        time = (element['dt'])
        # convert unix time to readable format
        time = datetime.utcfromtimestamp(time).strftime('%H:%M')

        # get temperature
        temperature = ((element['main'])['temp'])

        # get pressure
        pressure = ((element['main'])['pressure'])

        # get humidity
        humidity = ((element['main'])['humidity'])

        # get wheather description
        description = (((element['weather'])[0])['description'])

        # if there is a rain get value
        rain = None
        try:
            rain = ((element['rain'])['3h'])
        except:
            pass

        # if there is a snow get value
        snow = None
        try:
            snow = ((element['snow'])['1h'])
        except:
            pass

        # create weather object and assign values
        weather = Weather(time, temperature, pressure,
                          humidity, description, rain, snow)
        # append object to list
        weather_values.append(weather)

    return weather_values


if __name__ == "__main__":
    parse_data(get_json())
