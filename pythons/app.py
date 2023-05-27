from flask import Flask, request
from flask_cors import CORS
from timestamp_generator import *
import re

app = Flask(__name__)
CORS(app)
regexp = re.compile(r'https://www.youtube.com/watch\?v=')

@app.route('/', methods=['POST'])
def handle_data():
    data = request.get_json()  # get the data in JSON format
    if not regexp.search(data['url']):
        return {'status': 'error'}, 200
    print(data)  # print the data to the console or do something with it
    timestamps = generateTimestamps(data['url'], data['text'])
    print(timestamps)

    return {'status': 'success', 'timestamps': timestamps}, 200

if __name__ == '__main__':
    app.run(port=3000)  # run the server on port 3000