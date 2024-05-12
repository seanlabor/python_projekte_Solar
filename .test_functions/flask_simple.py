from flask import Flask
import schedule
import time
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

def stop_flask_app():
    print('juhu stopped')

schedule.every().day.at("17:54").do(stop_flask_app)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)