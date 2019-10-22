#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import datetime
import w1thermsensor

app = Flask(__name__, template_folder='templates')
@app.route("/")
def main():
   now = datetime.datetime.now()
   sensor=w1thermsensor.W1ThermSensor()
   temp = sensor.get_temperature()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'Pi Temperature Monitor',
      'time': timeString,
      'temperature' : temp
      }
   return render_template('main.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
