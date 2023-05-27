import json
import re


def getTimestamps(phrase,file):
    words, corpus = createDictionary(file)
    #print(words)
    searches = []
    times = []


    #find all extenstions of the word being searched (no phrases yet)
    for key, item in words.items():
        if key.startswith(phrase[0]):
            searches.append(key)
    print(searches)
    
    if searches:
        for search in searches:
            times += words[search]
        print(times)
        return times
    
    return [0]



def createDictionary(file):
    f = open(file)
    json_data = json.load(f)
    segments = json_data["segments"]
    corpus = re.sub(r'[^\w\s\d]+', '', json_data["text"])
    #key: word, value:[timestamps]
    timestamps = {}
    for segment in segments:
        for word in segment["words"]:

            text = re.sub(r'[^\w\s\d]+', '', word["text"])
            text = text.lower()
            if text not in timestamps:
                timestamps[text] = []
            timestamps[text].append(word["start"])
    return timestamps, corpus
