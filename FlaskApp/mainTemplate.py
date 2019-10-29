#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template

from flask_bootstrap import Bootstrap
import datetime
import MySQLdb
#import w1thermsensor
#import Adafruit_DHT

app = Flask(__name__, template_folder='templates')

bootstrap = Bootstrap(app)


@app.route("/")
def main():

  now = datetime.datetime.now()

  #sensor = w1thermsensor.W1ThermSensor()
  #sensor = w1thermsensor.W1ThermSensor()
  #temp = sensor.get_temperature()

  #sensor = Adafruit_DHT.DHT11
  #gpio = 17
  #humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

  timeString = now.strftime("%Y-%m-%d %H:%M")
  # temp_and_humidity = 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(
  #    temperature, humidity)
  templateData = {
      'title': 'Pi Temperature Monitor',
      'time': timeString,
      'temperature': '23',
      'temperature_and_humidity': '24'
  }
  return render_template('main.html', **templateData)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80, debug=True)
