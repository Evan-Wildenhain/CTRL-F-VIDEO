from flask import Flask, request
from flask_cors import CORS
from timestamp_generator import *
import re
import subprocess
import json
from model import *
import torch
from g2p_en import G2p
from faster_whisper import WhisperModel
if torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
elif torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")
model_size = "medium"
model_whisper = WhisperModel(model_size, device=str(DEVICE), compute_type="float16")


app = Flask(__name__)
CORS(app)
print(DEVICE)
regexp = re.compile(r'https://www.youtube.com/watch\?v=')
model = torch.load('model.pth')
model = model.to(DEVICE)
g2p = G2p()



@app.route('/', methods=['POST'])
def handle_data():
    data = request.get_json()
    if not regexp.search(data['url']):
        return {'status': 'error', 'message': 'invalid URL format'}, 400
    timestamps, extended_timestamps, phoneme_matches, similar_phonemes = generateTimestamps(data['url'], data['text'], model, g2p, model_whisper)

    return {'status': 'success', 'timestamps': timestamps,
             'extended_timestamps': extended_timestamps,
                'phoneme_matches': phoneme_matches,
                 'similar_phonemes': similar_phonemes}, 200

if __name__ == '__main__':
    app.run(port=3000)