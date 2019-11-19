import pymysql.cursors
import pymysql


def database_connection():
    # get credentials to connect with DB from file
    with open('FlaskApp/DB_credentials.txt') as file:
        credentials = file.readlines()
        user = credentials[0]
        password = credentials[1]
        db = credentials[2]
    connection = pymysql.connect(host='localhost',
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


# to do: change database time and date to datatime format!!!
# !!! move to DB file
# function to get data from DB i specified range of time
def query_to_get_rows(connection, hours, timestamp, value, table):
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
    query_result_list = [i[value] for i in query_result]

    return query_result_list


# function to convert list with time to readable string format
# time from query is in the datetime.timedelta format
# !!! move to DB file
def datatime_query(connection, hours, timestamp, value, table):
    # get data with time from query
    time_to_convert = query_to_get_rows(connection, hours, timestamp, value,
                                        table)
    # list to collect converted data
    readable_time = []
    # convert and add data to list
    for i in time_to_convert:
        if len(hours) == 1:
            hours = f'0{str(int(i.seconds/3600))}'
        if len(timestamp) == 1:
            minutes = f'0{str(int((i.seconds%3600)/60))}'
        readable_time.append(f'{hours}:{minutes}')

    return readable_time
