import matplotlib.pyplot as plt
from datetime import datetime
import database_handling as db


# function to draw linear plot
def draw_linear_plot(xdata, ydata, xlabel, ylabel, color, ticks):
    """Draw and save linear plot.

    Parameters:
        xdata(list):List with data for x axis of chart.
        ydata(list):List with data for y axis of chart.
        xlabel(string):Label for x axis.
        ylabel(string):Label for y axis.
        color(string):Color for line of plot.
        ticks(int):Number of ticks on x axis.


    """
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
    connection = db.database_connection()

    # variables to draw plots from last 23 hours
    time_period = 23
    timestamp = 5
    ticks = 24

    # get list of outside temperature values from 23 last hours
    outside_temperature = db.query_to_get_rows(connection, time_period,
                                               timestamp, 'temperature',
                                               'outside_temperature')
    # get list of inside temperature values from 23 lat hours
    inside_temperature = db.query_to_get_rows(connection, time_period,
                                              timestamp, 'temperature',
                                              'inside_temperature')
    # get list of time needed for x axis of plot from 23 lat hours
    time = db.datatime_query(connection, time_period, timestamp, 'hour',
                             'outside_temperature')
    # get list of humidity values from 23 lat hours
    humidity = db.query_to_get_rows(connection, time_period, timestamp,
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
