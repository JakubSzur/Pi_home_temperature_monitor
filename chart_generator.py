import pymysql.cursors
import pymysql
import matplotlib.pyplot as plt
from datetime import datetime


# connect to database !!! move to DB file
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
def datatime_query(hours, timestamp, value, table):
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


# function to draw linear plot
def draw_linear_plot(xdata, ydata, xlabel, ylabel, color, ticks):
    # draw linear plot with x and y data with specified color
    plt.plot(xdata, ydata, color=color)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    # show grid on plot
    plt.grid(True)
    ax = plt.axes()
    # set number of ticks on x axis
    ax.xaxis.set_major_locator(plt.MaxNLocator(ticks))
    # set rotation of ticks
    plt.xticks(rotation=70)
    # create name of png file to save
    now = datetime.now()
    date_time = now.strftime("%m:%d:%Y")
    # save fiel to specific path
    plt.savefig(f'FlaskApp/static/charts/{date_time}_{ylabel}.png', dpi=400)
    # close matplotlib
    plt.close('all')


if __name__ == "__main__":

    # connect to database
    connection = database_connection()

    # variables to draw plots from last 23 hours
    time_period = 23
    timestamp = 5
    ticks = 24

    # get list of outside temperature values from 23 last hours
    outside_temperature = query_to_get_rows(connection, time_period, timestamp,
                                            'temperature',
                                            'outside_temperature')
    # get list of inside temperature values from 23 lat hours
    inside_temperature = query_to_get_rows(connection, time_period, timestamp,
                                           'temperature',
                                           'inside_temperature')
    # get list of time needed for x axis of plot from 23 lat hours
    time = datatime_query(time_period, timestamp, 'hour',
                          'outside_temperature')
    # get list of humidity values from 23 lat hours
    humidity = query_to_get_rows(connection, time_period, timestamp,
                                 'humidity', 'inside_humidity')

    # generate outside tempearature plot
    draw_linear_plot(time, outside_temperature, 'time',
                     'outside temperature', 'midnightblue', ticks)
    # generate inside temperature plot
    draw_linear_plot(time, inside_temperature, 'time', 'inside_temperature',
                     'red', ticks)
    # generate humidity plot
    draw_linear_plot(time, humidity, 'time', 'humidity', 'slateblue', ticks)

    ''' to do: replace time list with date list
    # variables to draw plots from week
    time_period = 24*7

    get list of outside temperature values from 7 days
    outside_temperature = (query_to_get_rows(time_period, timestamp,
                           'temperature', 'outside_temperature'))
    get list of inside temperature values from from 7 days
    inside_temperature = (query_to_get_rows(time_period, timestamp,
                          'temperature', 'inside_temperature'))
    # to do: check type of data:
    # get list of date needed for x axis of plot from 7 days
    time = datatime_query(time_period, timestamp, 'hour',
                          'outside_temperature')
    # get list of humidity values from from 7 days
    humidity = query_to_get_rows(time_period, timestamp, 'humidity',
                                  'inside_humidity')

    # generate outside tempearature plot
    draw_linear_plot(date, outside_temperature, 'date', 'outside temperature',
                     'midnightblue')
    # generate inside temperature plot
    draw_linear_plot(date, inside_temperature, 'date', 'inside temperature',
                     'red')
    # generate humidity plot
    draw_linear_plot(time, humidity, 'time', 'humidity', 'slateblue')
    '''
