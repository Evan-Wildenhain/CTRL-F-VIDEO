import yt_dlp
import os
import re
from translate import translateVideo
from word_search import *
def generateTimestamps(url, phrase):

    phrase = phrase.split(" ")

    #grab current path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = f'{dir_path}\\audios'
    
    if not os.path.exists(path):
        os.makedirs(path)

    #grabs all after the last occurance of a '=' 
    #guaranteed to exist due to the function not being called unless
    #youtube url with watch?v= exists
    url_id = re.search(r'.*=(.*)$', url)
    url_id = url_id.group(1)

    # TODO: PUT LOGIC TO CHECK IF A JSON ALREADY EXISTS. IF IT DOES
    # THEN NO NEED TO GENERATE CUTS WE JUST RETURN THE VALUES IN THE JSON
    # BUT FOR NOT WE WILL DO EACH TIME
    if os.path.exists(f'{path}\{url_id}.json'):
        print("skipped")
        timestamps = getTimestamps(phrase,f'{path}\{url_id}.json')
        return timestamps
    
    downloadAudio(url,f'{path}\{url_id}')
    translateVideo(path,f'{path}\{url_id}',url_id)
    timestamps = getTimestamps(phrase,f'{path}\{url_id}.json')


    return timestamps


#Uses youtube-dlp to download audio to a temporary folder
# with the name of the YT-ID so it will always be unique
def downloadAudio(url, path):
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