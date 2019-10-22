#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import datetime
app = Flask(__name__, template_folder='templates')
@app.route("/")
def main():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
   return render_template('main.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
