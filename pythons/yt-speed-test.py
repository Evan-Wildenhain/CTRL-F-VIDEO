import time
import yt_dlp

# Hardcoded values for the video URL and output path
video_url = "placeholder for copywrite stuff"  # Replace this with your URL
output_path = "temp/"  # Replace this with your output directory

# Define the audio formats to convert to
formats = ['wav', 'mp3', 'flac']

# Download the audio and convert it to each format
for format in formats:
    print(f"Converting to {format}...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192',
        }],
        'outtmpl': output_path + '/translate.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        start_time = time.time()
        ydl.download([video_url])
        end_time = time.time()

    print(f"Conversion to {format} completed in {end_time - start_time} seconds.")
