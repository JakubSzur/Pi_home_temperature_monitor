import w1thermsensor
import time
import datetime

# check temperature in 5 minutes interval
while True:
    sensor = w1thermsensor.W1ThermSensor()
    temp = sensor.get_temperature()
    now = datetime.datetime.now()
    print(temp)
    time.sleep(300)
