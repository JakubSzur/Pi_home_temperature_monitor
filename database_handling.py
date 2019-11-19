import pymysql.cursors
import pymysql


def database_connection():
    """Connect with database.

    Parameters in DB_credentials.txt file:
        first line:User name, default user name - "user"
        second line:Password, default password - "root"
        third line:Name of database, default name - "DB"
    Returns:
        connection(object):Object to connect with database


    """
    # get credentials from txt file to connect with DB
    with open('FlaskApp/DB_credentials.txt') as file:
        credentials = file.readlines()
        user = credentials[0].split('\n')[0]
        password = credentials[1].split('\n')[0]
        db = credentials[2].split('\n')[0]
    connection = pymysql.connect(host='localhost',
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def create_tables(connection, tables):
    """Create tables if not exists.

    Parameters:
        connection (obj):Object returned from database_connection().
        tables(list):List with name of tables to create.
    Returns:
        query_result_list(list):List with values from query.


    """
    with connection.cursor() as cursor:
        # create tables if not exists
        for table in tables:
            sql = (f'CREATE TABLE IF NOT EXISTS {table} \
                (id int NOT NULL AUTO_INCREMENT, temperature double, \
                    day date, hour time, PRIMARY KEY (id))')
            cursor.execute(sql)


# to do: change database time and date to datatime format!!!
def query_to_get_rows(connection, hours, timestamp, value, table):
    """Get data from database in specified range of time.

    Parameters:
        connection (obj):Object returned from database_connection().              
        hours(int):Period of time in hours to get data from database.
        timestamp(int):Interval of measuremnts.
        value(string):Value to get from database table.
        table(string):Table with data in database.
    Returns:
        query_result_list(list):List with values from query.


    """
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


def datatime_query(connection, hours, timestamp, value, table):
    """Get measure time from database in range and convert to readable format.

    Parameters:
        connection (obj):Object returned from database_connection().
                         function
        hours(int):Period of time in hours to get data from database.
        timestamp(int):Interval of measuremnts.
        value(string):Value to get from database table.
        table(string):Table with data in database.
    Returns:
        query_result_list(list):List with values from query.


    """
    # get data with time in datetime.timedelta format from query
    time_to_convert = query_to_get_rows(connection, hours, timestamp, value,
                                        table)
    # list to collect converted data
    readable_time = []
    # convert and add data to list
    for i in time_to_convert:
        if len(str(hours)) == 1:
            hours = f'0{str(int(i.seconds/3600))}'
        if len(str(timestamp)) == 1:
            minutes = f'0{str(int((i.seconds%3600)/60))}'
        readable_time.append(f'{hours}:{minutes}')

    return readable_time


if __name__ == "__main__":
    pass
