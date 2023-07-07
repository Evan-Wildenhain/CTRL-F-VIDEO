import json
import re
import pickle
from g2p_en import G2p
from similar_words import *
import time


def getPhraseTimestamps(phrase,file):
    words = createDictionary(file)
    searches = []
    times = []
    print(phrase)

    #all words exist in the dict
    for word in phrase:
        if word not in words:
            return [[],[],[],[]]
        
   

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
    return [times,[],[],[]]

def getSingleWordTimestamps(word,file, pkl_file, model):
    g2p = G2p()
    phonetic_conversion = tuple(g2p(word[0]))
    with open(pkl_file, 'rb') as f:
        phonetic_keys = pickle.load(f)
    
    words= createDictionary(file)
    exact_matches = []
    extended_matches = []
    phoneme_matches = []
    similar_phonemes = []

    identical_phonemes_search = findIdenticalPhonetics(word=word[0],phonetic_keys=phonetic_keys, words=words, phonetic_conversion=phonetic_conversion)
    extended_words_search,exact_search  = findWordAndExtendedWords(word=word[0], words=words)
    similar_search = findSimilarsoundingWords(word[0],r'model.pth',phonetic_keys,words, phonetic_conversion, model)
    all_searches = identical_phonemes_search | extended_words_search | exact_search | similar_search

    
    #print("EXACT SEARCHES", exact_search)
    #print("IDENTICAL PHONETICS", identical_phonemes_search)
    #print("EXTENDED SEARCH", extended_words_search)
    #print("SIMILAR WORDS", similar_search)
    print("ALL", all_searches)

    while all_searches:
        search = all_searches.pop()
        for t in words[search]:
            if search == word[0]:
                exact_matches.append(t[1])
            elif search in identical_phonemes_search:
                phoneme_matches.append(t[1])
            elif search in extended_words_search:
                extended_matches.append(t[1])
            elif search in similar_search:
                similar_phonemes.append(t[1])

        
    return [exact_matches,extended_matches,phoneme_matches, similar_phonemes]



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
