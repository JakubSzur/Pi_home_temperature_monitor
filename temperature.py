import w1thermsensor
import w1thermsensor.errors
import time
from datetime import datetime
import pymysql.cursors
import pymysql
import Adafruit_DHT
import Adafruit_DHT.errors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='PiTemperature',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# to do - find better way to make parametric table
def insert_to_SQL_table(table_name, data):
    with connection.cursor() as cursor:
        sql = f"INSERT INTO {table_name} VALUES (%s,%s,%s)"
        insert_tuple = (str(data), date, hour)
        cursor.execute(sql, insert_tuple)
        print(
            f"Data saved: {table_name}:\
                {data}; date: {date}; time: {hour}")


# create tables to store data from sensors
with connection.cursor() as cursor:
    # create table outside_temperature if not exists
    sql = ('CREATE TABLE IF NOT EXISTS outside_temperature \
           (temperature double, day date, hour time)')
    cursor.execute(sql)
    print('Table outside_temperature created!')

    # create table inside_temperature if not exists
    sql = ('CREATE TABLE IF NOT EXISTS inside_temperature \
           (temperature double, day date, hour time)')
    cursor.execute(sql)
    print('Table inside_temperature created!')

    # create table inside_humidity if not exists
    sql = ('CREATE TABLE IF NOT EXISTS inside_humidity \
           (humidity double, day date, hour time)')
    cursor.execute(sql)
    print('Table inside_humidity created!')

# check temperature and write to database in interval
while True:

    # get date
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')

    # get hour
    hour = now.strftime('%H:%M')

    # get outside temperature from sensor
    try:
        sensor = w1thermsensor.W1ThermSensor()
        outside_temp = sensor.get_temperature()

    except w1thermsensor.errors:
        outside_temp = 'NULL'

    # get inside temperature and humidity from  sensor
    try:
        sensor = Adafruit_DHT.DHT11
        gpio = 17

    except Adafruit_DHT.errors:
        inside_temp = 'NULL'
        humidity = 'NULL'

    # write data to database
    try:
        with connection.cursor() as cursor:
            # write to outside_temperature table
            sql = "INSERT INTO outside_temperature VALUES (%s,%s,%s)"
            insert_tuple = (str(outside_temp), date, hour)
            cursor.execute(sql, insert_tuple)
            print(
                f"Data saved: outside temperature:\
                {outside_temp}; date: {date}; time: {hour}")

            # write to inside_temperature table
            sql = "INSERT INTO inside_temperature VALUES (%s,%s,%s)"
            insert_tuple = (str(inside_temp), date, hour)
            cursor.execute(sql, insert_tuple)
            print(
                f"Data saved: inside temperature:\
                {inside_temp}; date: {date}; time: {hour}")

            # write to inside_humidity table
            sql = "INSERT INTO inside_humidity VALUES (%s,%s,%s)"
            insert_tuple = (str(humidity), date, hour)
            cursor.execute(sql, insert_tuple)
            print(
                f"Data saved: inside humidity:\
                {humidity}; date: {date}; time: {hour}")

            connection.commit()

    finally:
        pass
        # connection.close()
    # check temperature every 5 minutes
    time.sleep(300)
