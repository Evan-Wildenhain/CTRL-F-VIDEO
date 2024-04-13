# CTRL-F for videos
**An audio to text word search**

### How to run
* import the folder into chrome extensions using the load unpacked function
* "python app.py" while in the pythons folder this will start a flask API that allows the model to run locally on your gpu.
* Go to a youtube url, clikc the extension type in a word or phrase or subword and click mark video.
* Mark Video - shows direct matches in the color green
* Show similar shows similar in levenshtein distance and phonetic similarity in the color purple (not that good)
* Show all - show both green and purple
* Remove stamps - sometimes it carries over to other youtube pages and just sits on the timebar (only visible when timebar is up), but this is just for those when you want to wipe the colored stamps.

![image](https://github.com/Evan-Wildenhain/CTRL-F-VIDEO/assets/66094938/2dff081b-59a3-49df-8fbb-e3b132da0992)



### About CTRL-F
* The purpose is to create an easy way to search videos for specific words/phrases
* Before whisper a lot of massaging and similarity searching was required to bring accuracy up, and while implemented they are rarely utilized due to the effectiveness of whisper

### Features
* Audio to text conversion using OpenAI whisper, credit to those at [faster-whisper](https://github.com/SYSTRAN/faster-whisper) for drastically improving speed over base whisper models.
* json storage of results for subsequent searches on a url
* phonetic similarity option (pretty much useless due to the effectiveness of whisper)
* timebar highlight of location in video on youtube

### Bugs/Limitations
* Only works for youtube as of now
* First search will not highlight the timebar while the model is running if you leave the page (simply search it again and the cached results will be instant)



### Efficiency
* RTX 3090 can do a 5 minute video in approximately 16 seconds


Feel free to take the project make it your own, this was just a small side project for me.
