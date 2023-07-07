import whisper_timestamped as whisper
from g2p_en import G2p
from collections import defaultdict
import os
import json
import re
import torch
import shutil
import pickle
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#Translates video using base model, currently does not support
#using multiGPU, but will create a branch that would allow for this down the road
def translateVideo(path,audio_path,url_id):
    model = whisper.load_model("base", device=DEVICE)
    for filename in os.listdir(audio_path):
        audio = whisper.load_audio(f'{audio_path}\{filename}')
        result = whisper.transcribe(model,audio,language="en")
        with open(f'{path}\{url_id}.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    shutil.rmtree(audio_path)
    return

#I'd love to be able to do this at the same time of the translation
#will look into it.
def createPhoneticDictionary(path, url_id):
    words = set()
    file = f'{path}\{url_id}.json'
    f = open(file)
    json_data = json.load(f)
    segments = json_data["segments"]

    for segment in segments:
        for word in segment["words"]:
            text = re.sub(r'[^\w\s\d]+', '', word["text"])
            text = text.lower()
            words.add(text)

    phonetic_dictionary = {}
    g2p = G2p()

    for word in words:
        phonetic_dictionary[word] = g2p(word)

    phonetic_keys = defaultdict(list)

    for key,value in sorted(phonetic_dictionary.items()):
        phonetic_keys[tuple(value)].append(key)

    with open(f'{path}\{url_id}-g2p.pkl', 'wb') as fp:
        pickle.dump(phonetic_keys, fp)
    return 
