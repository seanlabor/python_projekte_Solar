from InfluxDBCall import InfluxCall
import logging
import schedule

logging.basicConfig(encoding='utf-8', level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)



InfluxCaller = InfluxCall()

from flask import Flask, Response
from threading import Thread
from time import sleep

app = Flask(__name__)

stop_run = False


def boiler_function():

    global stop_run
    while not stop_run:
        print("Application is started and running...")
        current_power = InfluxCaller.get_active_power()
        print(current_power)
        #current_temp = get_temperatur()
        # if current_power > 4500 and current_temp < 60 :
            #boiler_on()
            # sleep(120)
        schedule.run_pending()
        sleep(5)



def run_wrapper():
    t = Thread(target=boiler_function)
    t.start()
    return "Processing"


@app.route("/stop", methods=['GET'])
def set_stop_run():
    global stop_run
    stop_run = True
    print("Application stopped")
    return "Application stopped"
schedule.every().day.at("18:38").do(set_stop_run) #NOTE Must be at this exact location to work, after set_stop_run()


@app.route("/run", methods=['GET'])
def run_process():
    global stop_run
    stop_run = False
    return Response(run_wrapper(), mimetype="text/html")


if __name__ == "__main__":

    app.run()
