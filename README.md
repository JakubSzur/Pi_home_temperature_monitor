# Raspberry Pi home temperature monitor

## General info

Project of raspberry pi connected with temperature and humidity sensors to monitor this values at home and outside.

Measurement of outside temperature, inside temperature and inside humidity is writing to MySQL database.
User can see measurement throught Flask WebServer running on raspberry Pi.
Flask WebServer is connected with OpenWeather API and getting information about forecast of weather of the following 24 hours.
After every day of measurements statistics in form of charts in period of last day and week are generated and displayed in WebService.

## Bill of materials

* Raspberry Pi Zero
* Waterproof DS18B20 temperature digital sensor
* DHT11–Temperature and Humidity Sensor
* 2x  4.7k resistor

## Technologies

* Python version: 3.7
* MySQL/MariaDB
* Flask
* Raspberry Pi Zero

## Python packages

* Flask
* pymysql
* matplotlib
* schedule
* w1thermsensor
* Adafruit_DHT