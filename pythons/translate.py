import whisper_timestamped as whisper
import os
import json
import torch
import shutil
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#Translates video using base model, currently does not support
# using multiGPU, but will create a branch that would allow for this down the road
def translateVideo(path,audio_path,url_id):
    model = whisper.load_model("base", device=DEVICE)
    for filename in os.listdir(audio_path):
        print(filename)
        audio = whisper.load_audio(f'{audio_path}\{filename}')
        result = whisper.transcribe(model,audio,language="en")
        with open(f'{path}\{url_id}.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    shutil.rmtree(audio_path)
    return
