from flask import Flask, request
from datetime import datetime
from influxDBCall import InfluxDBClient
import logging
import time
import os
import glob
import time
#import RPi.GPIO as GPIO

logging.basicConfig(filename="logs_boiler.log", encoding='utf-8', level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
"""os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
"""
# Set up GPIO mode
#GPIO.setmode(GPIO.BCM)

# Set up the GPIO pin
your_pin_number = 3  # Replace with your actual GPIO pin number
#GPIO.setup(your_pin_number, GPIO.OUT)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c



def are_dates_on_same_day(date1, date2):
    return date1.year == date2.year and date1.month == date2.month and date1.day == date2.day

app = Flask(__name__)

# Create InfluxDB client
client = InfluxDBClient(host = "192.168.178.65",
                        port = 8086,
                        username = "",      
                        password = "", 
                        database = "solaranzeige" )

# Test the connection
try:
    client.ping()
    logging.info("Connected to InfluxDB!")
except Exception as e:
    logging.warning("Unable to connect to InfluxDB:", str(e))




def get_Leistung_from_influx(client):
    # Query data from InfluxDB
    query = 'SELECT Leistung from PV order by time DESC Limit 1'  # Replace with your measurement name
    result = client.query(query)
    # Print the query result
    for point in result.get_points():
        parsed_time = datetime.strptime(point['time'], "%Y-%m-%dT%H:%M:%SZ")    
    client.close()
    return point['Leistung'], parsed_time

def check_day(date1, date2):
    """Check if still day of activation"""
    return date1.year == date2.year and date1.month == date2.month and date1.day == date2.day


temp = 20

boiler_on = False


@app.route('/start', methods=['POST'])
def handle_start():
    
    # Get the JSON data from the POST request
    global boiler_on
    boiler_on = True

    # command: curl -X POST -H "Content-Type: application/json" -d '{"key": "boileroff"}' http://127.0.0.1:5000/webhook
    # command: curl -X POST -H "Content-Type: application/json" -d '{"key": "boileron"}' http://127.0.0.1:5000/start

    app.logger.info("POST Request erhalten Boilerscript wird gestartet")
    leistung, parsed_time = get_Leistung_from_influx(client)
    script_day = parsed_time

    while check_day(script_day, datetime.today()) and boiler_on: #TODO test time constraint
        leistung, _ = get_Leistung_from_influx(client)
        print("boiling", leistung)
        time.sleep(5)
        #if leistung > 4000 and read_temp() < 60:
        if leistung > 4000 and temp < 60:
            app.logger.info("PV Leistung über 4000 Watt, Boiler wird aufgeheizt")
            #GPIO.output(your_pin_number, GPIO.HIGH)
            time.sleep(60)
        if temp > 60:
            #GPIO.output(your_pin_number, GPIO.LOW)
            app.logger.info("Boiler ist auf 60°C aufgeheizt. Heizung aus. Sleepy time ...")
            time.sleep(1800)
            
    if not check_day(script_day, datetime.today()):
        app.logger.info("Tag zu Ende. Boiler Script wird beendet")
        return "OK"
    app.logger.info("Boiler Script wird beendet")
    return "OK"
    
    

@app.route('/stop', methods=['POST'])
def handle_stop():

    logging.info("POST Request erhalten Boilerscript wird abgeschaltet")
    #GPIO.output(your_pin_number, GPIO.LOW)
    global boiler_on
    print("stopping")
    logging.info("Stopbefehl erhalten. Boiler aufheizen über Solaranzeige manuell gestoppt")
    boiler_on = False

    return "OK"



if __name__ == '__main__':
    app.run(debug=True)