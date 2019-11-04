#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template

import datetime
import pymysql.cursors
import pymysql

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
  return render_template('main.html', **templateData)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80, debug=True)
