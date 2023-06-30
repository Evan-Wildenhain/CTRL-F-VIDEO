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
    timestamps, extended_timestamps, similar_timestamps = generateTimestamps(data['url'], data['text'])
    print(timestamps)
    print(extended_timestamps)
    print(similar_timestamps)

    return {'status': 'success', 'timestamps': timestamps, 'extended_timestamps': extended_timestamps, 'similar_timestamps': similar_timestamps}, 200

if __name__ == '__main__':
    app.run(port=3000)  # run the server on port 3000