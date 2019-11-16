#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for

import datetime
import pymysql.cursors
import pymysql
import OpenWeatherAPI
import get_chart_path

app = Flask(__name__, template_folder='templates')


@app.route("/")
def main():

  # get current time
  now = datetime.datetime.now()
  timeString = now.strftime("%Y-%m-%d %H:%M")

  # connect to database
  connection = pymysql.connect(host='localhost',
                                user='root',
                                password='root',
                                db='PiTemperature',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

  # write querry to find last record from DB
  with connection.cursor() as cursor:
    # get outside temperature
    sql = ('SELECT temperature FROM  outside_temperature ORDER BY\
                ID DESC LIMIT 1')
    cursor.execute(sql)
    outside_temperature = cursor.fetchone()['temperature']

    # get inside temperature
    sql = ('SELECT temperature FROM  inside_temperature ORDER BY\
                ID DESC LIMIT 1')
    cursor.execute(sql)
    inside_temperature = cursor.fetchone()['temperature']

    # get inside humidity
    sql = ('SELECT humidity FROM  inside_humidity ORDER BY\
                ID DESC LIMIT 1')
    cursor.execute(sql)
    inside_humidity = cursor.fetchone()['humidity']

  templateData = {
      'title': 'Pi Temperature Monitor',
      'time': timeString,
      'outside_temperature': outside_temperature,
      'inside_temperature': inside_temperature,
      'inside_humidity': inside_humidity
  }

  # get JSON file with weather forecast
  get_JSON_file = OpenWeatherAPI.get_json()
  parsed_JSON = OpenWeatherAPI.parse_data(get_JSON_file)

  # iterate througth list with weather values and add
  # them to the dictionary
  for i in range(len(parsed_JSON)):
    templateData[f'time{i+1}']=parsed_JSON[i].time
    templateData[f'temp{i+1}']=parsed_JSON[i].temperature
    templateData[f'desc{i+1}']=parsed_JSON[i].description
    templateData[f'pressure{i+1}']=parsed_JSON[i].pressure
    templateData[f'humidity{i+1}']=parsed_JSON[i].humidity
    try:
      templateData[f'rain{i+1}']=parsed_JSON[i].rain
    except:
      pass
    templateData[f'snow{i+1}']=parsed_JSON[i].snow
  
  # get list with paths
  list_with_chart_paths = get_chart_path.find_charts('static/img',6)
  # begining of url_for formula to join with image path
  url_for_string  = 'src=\"{{url_for(\'static\', filename=\')'

  # add paths to dictionary to display charts
  chart_names = get_chart_path.get_chart_name(list_with_chart_paths)

  for i in list_with_chart_paths:

    for k in chart_names:
      if k in i:
        # change space to underscore
        k.replace(' ','_')
        # write url_for formula to dictionary
        templateData[f'{k}_chart']=f'\"{url_for_string}/{i}\')}}\"'

  return render_template('main.html', **templateData)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80, debug=True)
