import w1thermsensor
import time
import datetime
import pymysql.cursors
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# check temperature in 5 minutes interval
while True:
    sensor = w1thermsensor.W1ThermSensor()
    temp = sensor.get_temperature()
    now = datetime.datetime.now()
    print(temp)
    time.sleep(300)
