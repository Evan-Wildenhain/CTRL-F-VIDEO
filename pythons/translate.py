#import whisper_timestamped as whisper
from faster_whisper import WhisperModel
from g2p_en import G2p
from collections import defaultdict
import os
import json
import re
import torch
import shutil
import time
import pickle
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_size = "base"


#All this JSON logic is done due to the fact that switching over from Whisper
#To faster whisper caused it to be formatted differently
#So i formatted it the old way rather than rewrite all the logic for everything else.
def listToSegment(segment_list):
    segment_keys = [
        "id", "seek", "start", "end", "text", "tokens", "temperature", 
        "avg_logprob", "compression_ratio", "no_speech_prob", "words"
    ]
    word_keys = ["start", "end", "text", "probability"]
    segment_dicts = []
    for segment in segment_list:
        segment_dict = dict(zip(segment_keys, segment[:-1]))
    
        segment_dict["words"] = [dict(zip(word_keys, word)) for word in segment[-1]]

        segment_dicts.append(segment_dict)
    
    return segment_dicts


#Translates video using base model, currently does not support
#using multiGPU, but will create a branch that would allow for this down the road
def translateVideo(path,audio_path,url_id):
    """
    Transcribes the audio of a YouTube video using a pre-loaded model.

    Args:
        path (str): Path where the transcription JSON file will be stored.
        audio_path (str): Path of the audio file to transcribe.
        url_id (str): YouTube video ID, used to name the output JSON file.

    Returns:
        None: The function operates by side effect, transcribing the audio 
              and saving the transcription to a JSON file at the specified path.
    """

    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    for filename in os.listdir(audio_path):
        print("model running")
        start_time = time.time()
        #Current bug exists in whisper need to keep temp 0 or else program crashes from windows system
        segments, info = model.transcribe(f'{audio_path}\{filename}', beam_size=5, word_timestamps=True, temperature =0)
    segments = listToSegment(list(segments))
    json_dict = {
        "text": "Placeholder.",
        "segments": segments,
        "language": "en"
    }
    
    with open(f'{path}\{url_id}.json', 'w', encoding='utf-8') as f:
            json.dump(json_dict, f, ensure_ascii=False, indent=2)
    print("--- %s seconds for model conversion ---" % (time.time() - start_time))

    shutil.rmtree(audio_path)
    return

#I'd love to be able to do this at the same time of the translation
#will look into it.
def createPhoneticDictionary(path, url_id):
    """
    Creates a phonetic dictionary for the transcribed words of a YouTube video.

    Args:
        path (str): Path of the directory containing the transcription JSON file.
        url_id (str): YouTube video ID, used to name the output pickle file.

    Returns:
        None: The function operates by side effect, creating a phonetic dictionary 
              and saving it to a pickle file at the specified path.
    """
    words = set()
    file = f'{path}\{url_id}.json'
    f = open(file)
    json_data = json.load(f)
    segments = json_data["segments"]

    for segment in segments:
        for word in segment["words"]:
            text = re.sub(r'[^\w\d]+', '', word["text"])
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
