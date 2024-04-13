# CTRL-F for videos
**An audio to text word search**

### How to run
"python app.py" while in the pythons folder.

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
