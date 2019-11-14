import urllib.request
import json
from datetime import datetime

# class to collect wheather values
class Weather:

    def __init__(self, time, temperature, pressure, humidity, description
                    rain='no data', snow='no data'):
        self.time = time
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.description = description
        self.rain = rain
        self.snow = snow


# function to get JSON with weather forecast
def get_json():
    # get API key from file to connect with API
    with open('APPID.txt') as file:
        api_key = file.readline()
    # get json with hourly forecast from Openwheather API
    with urllib.request.urlopen('http://api.openweathermap.org//data//2.5/' \
                                f'forecast/?id=7531890&APPID={api_key}' \
                                '&units=metric') as url:
        data = json.loads(url.read().decode())
    return data


# get specific values from JSON
def parse_data(json_file):
    # get forecast values from JSON file
    for element in json_file['list']:
        # get time
        time = (element['dt'])
        # convert unix time to readable format
        print(datetime.utcfromtimestamp(time).strftime('%H:%M'))
        # get temperature
        print((element['main'])['temp'])
        #get pressure
        print((element['main'])['pressure'])
        # get humidity
        print((element['main'])['humidity'])
        # get wheather description
        print(((element['weather'])[0])['description'])
        # if there is a rain get value
        try:
            print((element['rain'])['3h'])
        except: 
            pass
        # if there is a snow get value
        try:
            print((element['snow'])['1h'])
        except:
            pass

if __name__ == "__main__":
    parse_data(get_json())
