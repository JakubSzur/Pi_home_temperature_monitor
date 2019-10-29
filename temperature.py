import w1thermsensor
import time
import datetime
import pymysql.cursors
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='PiTemperatureda',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# check temperature and write to database in interval
while True:
        # get temperature from sensor
    sensor = w1thermsensor.W1ThermSensor()
    temp = sensor.get_temperature()
    # get date
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    # get hour
    hour = now.strftime('%H:%M')
    print(temp)

    try:
        # write data to database
        with connection.cursor() as cursor:
            sql = "INSERT INTO outside_temperature VALUES (%s,%s,%s)"
            insert_tuple = (str(temp), date, hour)
            cursor.execute(sql, insert_tuple)
            print(
                f"Data saved: temperature: {temp}; date: {date}; time: {hour}")
            connection.commit()

    finally:
        connection.close()
    # check temperature every 5 minutes
    time.sleep(300)
