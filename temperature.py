import w1thermsensor
import w1thermsensor.errors
import time
import Adafruit_DHT
import database_handling as db

# connect to database
connection = db.database_connection()

# create tables to store data from sensors
tables = ['outside_temperature', 'inside_temperature', 'inside_humidity']
db.create_tables(connection, tables)

# check temperature and write to database in interval
while True:

    # get outside temperature from sensor
    try:
        sensor = w1thermsensor.W1ThermSensor()
        outside_temp = sensor.get_temperature()

    except w1thermsensor.errors:
        outside_temp = 'NULL'

    # get inside temperature and humidity from  sensor
    sensor = Adafruit_DHT.DHT11
    gpio = 17
    humidity, inside_temp = Adafruit_DHT.read_retry(sensor, gpio)

    # if measure is wrong, write NULL value to record
    if humidity is None:
        humidity = 'NULL'
    elif inside_temp is None:
        inside_temp = 'NULL'

    # list with values
    values = [outside_temp, inside_temp, humidity]

    # write data to database
    db.insert_data(connection, tables, values)

    # check temperature in interval
    time.sleep(300)

connection.close()
