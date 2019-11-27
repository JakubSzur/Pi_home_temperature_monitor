from flask import Flask, render_template, url_for

import OpenWeatherAPI
import get_chart_path
from Pi_home_temperature_monitor import database_handling as db

app = Flask(__name__, template_folder='templates')


@app.route("/")
def main():

    # connect to database
    connection = db.database_connection()

    # get dictionary with last values from DB
    last_values = db.get_current_values(connection)

    templateData = {
        'title': 'Pi Temperature Monitor',
        'time': last_values['time'],
        'outside_temperature': last_values['outside_temperature'],
        'inside_temperature': last_values['inside_temperature'],
        'inside_humidity': last_values['inside_humidity']
        }

    # get JSON file with weather forecast
    get_JSON_file = OpenWeatherAPI.get_json()
    parsed_JSON = OpenWeatherAPI.parse_data(get_JSON_file)

    # iterate througth list with weather values and add
    # them to the dictionary
    for i in range(len(parsed_JSON)):
        templateData[f'time{i+1}'] = parsed_JSON[i].time
        templateData[f'temp{i+1}'] = parsed_JSON[i].temperature
        templateData[f'desc{i+1}'] = parsed_JSON[i].description
        templateData[f'pressure{i+1}'] = parsed_JSON[i].pressure
        templateData[f'humidity{i+1}'] = parsed_JSON[i].humidity
        try:
            templateData[f'rain{i+1}'] = parsed_JSON[i].rain
        except:
            pass
        templateData[f'snow{i+1}'] = parsed_JSON[i].snow

    # get list with paths
    list_with_chart_paths = get_chart_path.find_charts('static/img', 3)
    # begining of url_for formula to join with image path
    url_for_string = 'url_for(\'static\', filename=\''

    # add paths to dictionary to display charts
    chart_names = get_chart_path.get_chart_name(list_with_chart_paths)

    for i in list_with_chart_paths:

        for k in chart_names:
            if k in i:
                k = k.replace(' ', '_')
                templateData[f'{k}_chart'] = i
    return render_template('main.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
