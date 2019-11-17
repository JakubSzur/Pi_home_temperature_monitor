import schedule
import time
import os
import chart_generator.py

# run python file which collect data from sensors to DB
os.system('python3 temperature.py')

# run python file to start Flask webservice
os.system('python FlaskApp/mainTemplate.py')

# run python file to generate charts
generate_charts = os.system('python3 chart_generator.py')

# generate charts every dat at 00:00
while True:
    schedule.every().day.at('00:00').do(generate_charts)
    time.sleep(30)