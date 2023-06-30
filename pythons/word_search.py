import json
import re
from g2p_en import G2p


def getPhraseTimestamps(phrase,file):
    words, _ = createDictionary(file)
    searches = []
    times = []
    print(phrase)

    #all words exist in the dict
    for word in phrase:
        if word not in words:
            return [[0],[0],[0]]
        
   

    previous = [x for x in words[phrase[0]]]
    for word in phrase[1:]:
        current = [x for x in words[word]]
        curr_dict = {id2-1: time2 for id2, time2 in current}
        result = [(id1+1, time1) for id1,time1 in previous if id1 in curr_dict]
        previous = result

    times = [r[1] for r in result]
    return [times, [0], [0]]

def getSingleWordTimestamps(word,file):
    g2p = G2p()
    words, _ = createDictionary(file)
    searches = []
    phonetic_match = []
    exact_matches = []
    extended_matches = []
    similar_matches = []


    # optimize this later.
    for key, item in words.items():
        if key.startswith(word[0]):
            searches.append(key)
        if g2p(key) == g2p(word[0]):
            searches.append(key)
            phonetic_match.append(key)

    print(searches)
    print(phonetic_match)
    
    if searches:
        for search in searches:
            for time in words[search]:
                if search == word[0]:
                    exact_matches.append(time[1])
                elif search not in phonetic_match:
                    extended_matches.append(time[1])
                else:
                    similar_matches.append(time[1])
        
        return [exact_matches,extended_matches,similar_matches]
    
    return [[0],[0],[0]]



def createDictionary(file):
    f = open(file)
    json_data = json.load(f)
    segments = json_data["segments"]
    corpus = re.sub(r'[^\w\s\d]+', '', json_data["text"])
    #key: word, value:[(id,timestamp),(id,timestamp)]
    timestamps = {}
    val = 0
    for segment in segments:
        for word in segment["words"]:

            text = re.sub(r'[^\w\s\d]+', '', word["text"])
            text = text.lower()
            if text not in timestamps:
                timestamps[text] = []
            timestamps[text].append((val,word["start"]))
            val += 1
    return timestamps, corpus
