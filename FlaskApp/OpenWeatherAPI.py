import urllib.request
import json

# get API key from file to connect with API
with open('APPID.txt') as file:
    api_key = file.readline()

# get json with hourly forecast from Openwheather API
with urllib.request.urlopen('http://api.openweathermap.org//data//2.5/' \
                            f'forecast?id=7531890&APPID={api_key}' \
                             '&units=metric') as url:
    data = json.loads(url.read().decode())
