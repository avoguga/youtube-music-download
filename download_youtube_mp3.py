from flask import Flask, request
from flask_cors import CORS
from pytube import YouTube
import threading
import os
from pathlib import Path


app = Flask(__name__)
CORS(app)

def get_link_and_convert_at_mp3(link, destination):
    yt = YouTube(link)
    audio = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    print(f'Downloading {audio.title}')
    out_file = audio.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

def download_songs(urls):
    threads = []
    destination = str(Path.home() / "Downloads")
    # destination = './songs'
    for url in urls:
        t = threading.Thread(target=get_link_and_convert_at_mp3, args=(url, destination))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print('All files downloaded successfully!')

def save_urls_to_file(urls):
    with open('urls.txt', 'a') as f:
        for url in urls:
            f.write(f'{url},\n')

@app.route('/')
def hello():
    return 'Hello!'

@app.route('/post_youtube_url', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
        urls = data.get('urls')
        if urls:
            save_urls_to_file(urls)
            download_songs(urls)
            return 'Success!'
        else:
            return 'No URLs found in the JSON data.'
    else:
        return 'Content-Type not supported!'
    
if __name__ == "__main__":
    app.run()
