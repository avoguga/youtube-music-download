from pytube import YouTube
import threading
import os


threads = []
with open('urls.txt', 'r') as file:
    urls = [row.strip() for row in file]


def download_mp3(link):
    yt = YouTube(link)
    audio = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    destination = './MusicasPedroTexeira'
    print(f'Downloading {audio.title}')
    out_file = audio.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)


for i in range(len(urls)):
    t = threading.Thread(target=download_mp3, args=(urls[i],))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print('All files downloaded successfully!')