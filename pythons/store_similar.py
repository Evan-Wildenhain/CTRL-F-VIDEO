
import csv
from g2p_en import G2p
import pandas as pd
import numpy as np

def storeSimilar(word, words, g2p, phoneme):
    """
    Stores the results of the similar LSTM model in a new CSV. No similarity score is assigned.
    and no similarity 1 or 0 is assigned. This allows for easy human verification.
    someone can go through and assign similar or not values then this dataset can be used for fine tuning.
    Removes the need to think of new pairs.

    Args:
        word (str): string of the searched word
        word (list): List containing all found words
        g2p (function): allows for the conversion of words to phonemes
        phoneme (tuple): tuple of strings making up the phonetic structure of the searched word

    Returns:
        None: It writes into a csv.
    """
    if word in words:
        words.remove(word)
    words = list(words)
    data = []
    for i in range(len(words)):
        phoneme_i = tuple(g2p(words[i]))
        pair = sorted([(word,phoneme), (words[i], phoneme_i)], key=lambda x:x[0])
        data.append([pair[0][1], pair[1][1], pair[0][0], pair[1][0], -1, np.nan])
    
    df = pd.DataFrame(data,columns=["phoneme1", "phoneme2", "word1","word2", "similarity", "similar"])

    if pd.io.parsers.read_csv('train.csv').shape[0] != 0:
        df_old = pd.read_csv('train.csv')
        df_combined = pd.concat([df_old,df], ignore_index=True).drop_duplicates()
    else:
        df_combined = df

    df_combined.to_csv('train.csv', index=False)

    return
