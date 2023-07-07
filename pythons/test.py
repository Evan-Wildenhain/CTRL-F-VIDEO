import requests
import json

def testData(url, text):

    server_url = 'http://localhost:3000/'

    data = {'url': url, 'text': text}

    response = requests.post(server_url, json=data)

    if response.status_code != 200:
        print(f'Request failed with status {response.status_code}')
        return

    response_data = response.json()

    print(json.dumps(response_data, indent = 4))
    

if __name__ == "__main__":
    testData('https://www.youtube.com/watch?v=INjgdhFzIEY&t=3761s', 'one')