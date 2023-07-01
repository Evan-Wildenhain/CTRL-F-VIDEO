import json
import re
import pickle
from g2p_en import G2p


def getPhraseTimestamps(phrase,file):
    words = createDictionary(file)
    searches = []
    times = []
    print(phrase)

    #all words exist in the dict
    for word in phrase:
        if word not in words:
            return [[],[],[]]
        
   

    previous = [x for x in words[phrase[0]]]
    #finds the intersections of words where the id is curr id-1, since we order each word
    # in the translation
    #e.g. this is a test -> (11, this) (12, is) (13, a) (14, test) would be a match
    for word in phrase[1:]:
        current = [x for x in words[word]]
        curr_dict = {id2-1: time2 for id2, time2 in current}
        result = [(id1+1, time1) for id1,time1 in previous if id1 in curr_dict]
        previous = result

    times = [r[1] for r in result]
    return [times,[],[]]

def getSingleWordTimestamps(word,file, pkl_file):
    g2p = G2p()
    phonetic_conversion = tuple(g2p(word[0]))
    with open(pkl_file, 'rb') as f:
        phonetic_keys = pickle.load(f)
    words= createDictionary(file)
    searches = set()
    phonetic_match = set()
    exact_matches = []
    extended_matches = []
    similar_matches = []


    # optimize this later.
    # or dont im lazy
    for key, item in words.items():
        if key.startswith(word[0]):
            searches.add(key)

    if phonetic_conversion in phonetic_keys:
        for w in phonetic_keys[phonetic_conversion]:
            phonetic_match.add(w)
            searches.add(w)
    
    print("SEARCHES", searches)
    print("PHONETIC SEARCHES", phonetic_match)

    while searches:
        search = searches.pop()
        print(search)
        for time in words[search]:
            if search == word[0]:
                exact_matches.append(time[1])
            elif search not in phonetic_match:
                extended_matches.append(time[1])
            else:
                similar_matches.append(time[1])
        
    return [exact_matches,extended_matches,similar_matches]



def createDictionary(file):
    f = open(file)
    json_data = json.load(f)
    segments = json_data["segments"]
    #key: word, value:[(id,timestamp),(id,timestamp)]
    timestamps = {}
    val = 0
    for segment in segments:
        for word in segment["words"]:
            #remove all the punctuation and stuff like that then lower all text.
            text = re.sub(r'[^\w\s\d]+', '', word["text"])
            text = text.lower()
            if text not in timestamps:
                timestamps[text] = []
            timestamps[text].append((val,word["start"]))
            val += 1
    return timestamps
