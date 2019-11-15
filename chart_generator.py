import pymysql.cursors
import pymysql
import matplotlib.pyplot as plt

# connect to database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='PiTemperature',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def query_to_get_rows(hours, timestamp, value, table):
    # number of rows to get with measurement in timestamp of measurement
    rows = int((hours*60)/timestamp)
    
    # queries to get data from database
    with connection.cursor() as cursor:
        # get outside temperature from defined number of hours
        sql = (f'SELECT {value} FROM(SELECT * FROM {table} order by\
                id desc limit {rows})Var1 ORDER by id ASC')
        cursor.execute(sql)
        query_result = cursor.fetchall()

    # list to collect data from query
    query_result_list = []
    # add data from query to list
    for i in query_result:
        query_result_list.append(i[value])

    return (query_result_list)

if __name__ == "__main__":

    print(query_to_get_rows(24, 'temperature', 'outside_temperature', 5))
    print(query_to_get_rows(24, 'temperature', 'inside_temperature', 5))
    print(query_to_get_rows(24, 'humidity', 'inside_humidity', 5))