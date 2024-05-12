from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Get the JSON data from the POST request
    data = request.get_json()

    # Perform actions based on the received data
    print("Received POST request with data:", data)

    # Add your custom logic to process the data

    return "OK"

if __name__ == '__main__':
    app.run(debug=True)