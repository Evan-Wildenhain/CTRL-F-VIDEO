from flask import Flask, request
from flask_cors import CORS
from timestamp_generator import *
import re
import subprocess
import json
from model import *
import torch
from g2p_en import G2p
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


app = Flask(__name__)
CORS(app)
regexp = re.compile(r'https://www.youtube.com/watch\?v=')
model = torch.load('model.pth')
model = model.to(DEVICE)
g2p = G2p()

def getOutdatedPackages():
    outdated_packages = []
    output = subprocess.check_output(["pip", "list", "--outdated", "--format", "json"])
    outdated_packages_list = json.loads(output)

    for package in outdated_packages_list:
        outdated_packages.append(package['name'])

    return outdated_packages

def updatePackage(package_name):
    try:
        output = subprocess.check_output(["pip", "install", "--upgrade", package_name])
        print(f"Successfully updated {package_name}")
    except Exception as ex:
        print(f"Error occurred while trying to update {package_name}. Error: {str(ex)}")


def updatePackages():
    with open('requirements.txt', 'r') as f:
        required_packages = f.read().splitlines()

    outdated_packages = getOutdatedPackages()

    for package in outdated_packages:
        if package in required_packages:
            updatePackage(package)


@app.route('/', methods=['POST'])
def handle_data():
    data = request.get_json()
    if not regexp.search(data['url']):
        return {'status': 'error', 'message': 'invalid URL format'}, 400
    timestamps, extended_timestamps, phoneme_matches, similar_phonemes = generateTimestamps(data['url'], data['text'], model, g2p)

    return {'status': 'success', 'timestamps': timestamps,
             'extended_timestamps': extended_timestamps,
                'phoneme_matches': phoneme_matches,
                 'similar_phonemes': similar_phonemes}, 200

if __name__ == '__main__':
    with app.app_context():
        updatePackages()
    app.run(port=3000)