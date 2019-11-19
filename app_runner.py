import os


# run python file which collect data from sensors to DB
os.system('python3 temperature.py')

# run python file to start Flask webservice
os.system('python FlaskApp/mainTemplate.py')
