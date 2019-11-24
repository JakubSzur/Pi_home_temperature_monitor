import w1thermsensor
import w1thermsensor.errors
import pymysql.cursors
import pymysql
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
    try:
        with connection.cursor() as cursor:
            # write to outside_temperature table
            sql = "INSERT INTO outside_temperature VALUES (NULL,%s,%s,%s)"
            insert_tuple = (str(outside_temp), date, hour)
            cursor.execute(sql, insert_tuple)
            print(
                f"Data saved: outside temperature:\
                {outside_temp}; date: {date}; time: {hour}")

            # write to inside_temperature table
            sql = "INSERT INTO inside_temperature VALUES (NULL,%s,%s,%s)"
            insert_tuple = (str(inside_temp), date, hour)
            cursor.execute(sql, insert_tuple)
            print(
                f"Data saved: inside temperature:\
                {inside_temp}; date: {date}; time: {hour}")

            # write to inside_humidity table
            sql = "INSERT INTO inside_humidity VALUES (NULL,%s,%s,%s)"
            insert_tuple = (str(humidity), date, hour)
            cursor.execute(sql, insert_tuple)
            print(
                f"Data saved: inside humidity:\
                {humidity}; date: {date}; time: {hour}")

            connection.commit()

    except Exception:
        pass

    # check temperature in interval
    time.sleep(300)

connection.close()
