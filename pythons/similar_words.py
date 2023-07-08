import torch
import torch.nn as nn
import numpy as np
from g2p_en import G2p
from model import *
import torch.nn.functional as F
import time
from collections import defaultdict
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")



one_hot_dict = {'AA0': 0, 'AA1': 1, 'AA2': 2, 'AE0': 3, 'AE1': 4, 'AE2': 5, 'AH0': 6, 'AH1': 7, 'AH2': 8, 'AO0': 9, 'AO1': 10, 'AO2': 11, 'AW0': 12, 'AW1': 13, 'AW2': 14, 'AY0': 15, 'AY1': 16, 'AY2': 17, 'B': 18, 'CH': 19, 'D': 20, 'DH': 21, 'EH0': 22, 'EH1': 23, 'EH2': 24, 'ER0': 25, 'ER1': 26, 'ER2': 27, 'EY0': 28, 'EY1': 29, 'EY2': 30, 'F': 31, 'G': 32, 'HH': 33, 'IH0': 34, 'IH1': 35, 'IH2': 36, 'IY0': 37, 'IY1': 38, 'IY2': 39, 'JH': 40, 'K': 41, 'L': 42, 'M': 43, 'N': 44, 'NG': 45, 'OW0': 46, 'OW1': 47, 'OW2': 48, 'OY0': 49, 'OY1': 50, 'OY2': 51, 'P': 52, 'R': 53, 'S': 54, 'SH': 55, 'T': 56, 'TH': 57, 'UH0': 58, 'UH1': 59, 'UH2': 60, 'UW0': 61, 'UW1': 62, 'UW2': 63, 'V': 64, 'W': 65, 'Y': 66, 'Z': 67, 'ZH': 68}

def findIdenticalPhonetics(word, phonetic_keys, words, phonetic_conversion):
    """
    Identifies words with identical phonetic conversions.

    Args:
        word (str): The word to compare with others.
        phonetic_keys (dict): A dictionary mapping phonetic conversions to words.
        words (dict): A dictionary of words (unused in this function, may be deprecated).
        phonetic_conversion (tuple): Phonetic conversion of the input word.

    Returns:
        set: A set of words that have the same phonetic conversion as the input word.
    """

    identical_phonemes = set()
    if phonetic_conversion not in phonetic_keys:
        return identical_phonemes
    else:
        for w in phonetic_keys[phonetic_conversion]:
            if w != word:
                identical_phonemes.add(w)
    return identical_phonemes

def findWordAndExtendedWords(word, words):
    """
    Identifies words that start with the input word and exact matches.

    Args:
        word (str): The word to search for.
        words (dict): A dictionary of words.

    Returns:
        tuple: A tuple of two sets. The first set contains words that start with the input word
               (excluding the exact match), and the second set contains the exact match.
    """
    extended = set()
    exact = set()
    for key, item in words.items():
        if key.startswith(word) and key != word:
            extended.add(key)
        elif key == word:
            exact.add(key)
    return extended, exact



def oneHotEncode(word, conversion):
    """
    One hot encodes the phonemes of a word.

    Args:
        word (str): The word to be one hot encoded.
        conversion (dict): A dictionary mapping phonemes to integers.

    Returns:
        numpy.array: An array of one hot encoded phonemes of the word.
    """
    one_hot = []
    for phoneme in word:
        curr = np.zeros(69)
        curr[conversion[phoneme]] = 1
        one_hot.append(curr)
    return np.array(one_hot)

    

def evaluateModelByBatches(model,phonemes,phoneme_list,phonetic_keys):
    """
    Evaluates a model in batches to identify phonemes similar to the input using a siamese LSTM model.

    Args:
        model (model): The model used to evaluate similarity.
        phonemes (list): List of phonemes representing a word.
        phoneme_list (list): List of phonemes to compare with the input phonemes.
        phonetic_keys (dict): A dictionary mapping phonetic conversions to words.

    Returns:
        set: A set of words that sound similar to the input phonemes.
    """

    words_by_length = defaultdict(list)
    for phonetics in phoneme_list:
        words_by_length[len(phonetics)].append(phonetics)

    similar_phonemes = []
    similar_words = set()
    batch_size = 128

    word_encoded = oneHotEncode(phonemes, one_hot_dict)
    
    for length, words in words_by_length.items():
        word_encoded_batch = torch.stack([torch.tensor(word_encoded, dtype=torch.float32).to(DEVICE)] * len(words))
        compare_encoded_list = [oneHotEncode(word2, one_hot_dict) for word2 in words]
        compare_encoded_batch = torch.stack([torch.tensor(compare_encoded, dtype=torch.float32).to(DEVICE) for compare_encoded in compare_encoded_list])

        for i in range(0,len(words), batch_size):
            batch1 = word_encoded_batch[i:i+batch_size]
            batch2 = compare_encoded_batch[i:i+batch_size]
            with torch.no_grad():
                output = model(batch1, batch2)
                _, predicted = torch.max(output.data, 1)
                similar_indices = (predicted == 1).nonzero(as_tuple=True)[0]
                similar_phonemes.extend([words[i+index.item()] for index in similar_indices])
    for p in similar_phonemes:
        words = phonetic_keys[tuple(p)]
        for word in words:
            similar_words.add(word)
    return similar_words



def findSimilarsoundingWords(phonetic_keys, phonetic_conversion,model):
    """
    Identifies words that sound similar to the input word.

    Args:
        phonetic_keys (dict): A dictionary mapping phonetic conversions to words.
        phonetic_conversion (tuple): Phonetic conversion of the input word.
        model (model): A model used to find similar sounding words.

    Returns:
        set: A set of similar sounding words.
    """
    searchable_phonemes = []
    for key, value in phonetic_keys.items():
        if len(key) >= len(phonetic_conversion)-1 and len(key) <= len(phonetic_conversion) + 1:
            #Remove spaces if any in key for model.
            no_spaces = [x for x in key if x != ' ']
            searchable_phonemes.append(no_spaces)
    similar_words = evaluateModelByBatches(model,list(phonetic_conversion), searchable_phonemes, phonetic_keys)

    return similar_words
    