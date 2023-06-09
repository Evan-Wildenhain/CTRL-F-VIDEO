import yt_dlp
import os
import re
from translate import *
from word_search import *
import time

def generateTimestamps(url, phrase, model):
    """
    Generates timestamps for a given phrase in the audio of a YouTube video.

    Args:
        url (str): URL of a YouTube video.
        phrase (str): A space-separated string representing a phrase to search for.
        model (model): A model used to find similar sounding words.

    Returns:
        list: A list of timestamps where the phrase appears in the audio.
              If the phrase is a single word, returns four lists of timestamps for:
              [exact matches, extended matches, phoneme matches, similar phonemes].
              If the phrase consists of multiple words, returns timestamps where the 
              words appear in the same order as in the phrase.
    """

    phrase = phrase.split(" ")

    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = f'{dir_path}\\audios'
    
    if not os.path.exists(path):
        os.makedirs(path)

    #grabs all after the last occurance of a '=' 
    #guaranteed to exist due to the function not being called unless
    #youtube url with watch?v= exists
    #if you accidentally have timestamped url.
    url = url.split("&t=")[0]
    url_id = re.search(r'.*=(.*)$', url)
    url_id = url_id.group(1)

    if not os.path.exists(f'{path}\{url_id}.json'):
        downloadAudio(url,f'{path}\{url_id}')
        translateVideo(path,f'{path}\{url_id}',url_id)
    else:
        #Put logic to check if model has been updated here later.
        print("Already Downloaded")

    if not os.path.exists(f'{path}\{url_id}-g2p.pkl'):
        createPhoneticDictionary(path,url_id)
    else:
        print("Already phoneticised")

    if len(phrase) == 1:
        start_time = time.time()
        timestamps = getSingleWordTimestamps(phrase,f'{path}\{url_id}.json', f'{path}\{url_id}-g2p.pkl', model)
        print("--- %s seconds for entire search ---" % (time.time() - start_time))
    else:
        timestamps = getPhraseTimestamps(phrase,f'{path}\{url_id}.json')


    return timestamps


#Uses youtube-dlp to download audio to a temporary folder
# with the name of the YT-ID so it will always be unique
def downloadAudio(url, path):
    """
    Downloads the audio of a YouTube video using youtube-dlp.

    Args:
        url (str): URL of the YouTube video.
        path (str): Path where the audio file will be stored.

    Returns:
        None: The function operates by side effect, downloading the audio 
              and saving it to the provided path.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': path + '/translate.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

#Cuts the video into 30 second chunks if length > 30, with a
#sliding window value of 5 seconds
#this will only be used if we have multiple GPUs
#TODO: implement later since I don't have mGPUs at the moment.
def slidingWindowCuts(path):
    return