import os
import glob
from youtube_search import YoutubeSearch
from pytube import YouTube 
from pydub import AudioSegment
import moviepy.editor as mp
import multiprocessing
import threading
import time


def main(singer,n,cut):

    def task(i,cut,j):

        # SAVE_PATH = "C:/Users/DELL/OneDrive/Desktop/thapar/sixth sem/predictive analysis/rana sir/mashup_multithreading/downloaded" 
        # downloading videos
        try: 
            yt = YouTube(i) 
        except: 
            print("Connection Error") 
        
        d_video = yt.streams.filter(only_audio=True).first()
        
        try:
            out_file=d_video.download() 
        except:
            print("Download Failed")
            quit()
        
        # renaming videos
        base, ext = os.path.splitext(out_file)
        base='video'+str(j)
        new_file = base + ext
        os.rename(out_file, new_file)
        
        # converting mp4 to mp3
        try:
            audio = AudioSegment.from_file('video'+str(j) + "." + d_video.subtype, format=d_video.subtype)
        except:
            print("Error: Unable to convert mp4 to mp3.")

        output_filename = 'video'+str(j) + ".mp3"
        audio.export(output_filename, format="mp3")

        # cutting first n seconds
        audio = AudioSegment.from_file('video'+str(j) + ".mp3", format='mp3')

        first_n_seconds = audio[:cut * 1000]

        output_filename = "first_{}_seconds_{}.{}".format(cut, 'video'+str(j), 'mp3')
        first_n_seconds.export(output_filename, format='mp3')
        # removing unwanted files
        os.remove('video'+str(j) + ".mp3")
        os.remove('video'+str(j) + ".mp4")



# ----------------------------------------main function------------------------------------------------------


    startTime = time.time()
    numberOfThreads = multiprocessing.cpu_count()
    activeThreads = threading.activeCount()

    # youtube search
    # try:
    results = YoutubeSearch(singer, max_results=n).to_dict()
    # except:
    #     print("Youtube search failed")
    #     exit()

    url=[]
    for i in range(len(results)):
        url.append(results[i]['url_suffix'])
    j=1
    links=[]
    link="https://www.youtube.com"
    for i in range(len(results)):
        links.append(link+url[i])

    for i in links:
        t = threading.Thread(target=task , args=(i,cut,j))
        t.start()
        j=int(j)+1
        while True:
            if threading.activeCount() - activeThreads + 1 <= numberOfThreads:
                break
        time.sleep(1)

    while True:
        if threading.activeCount() == activeThreads:
            files = glob.glob("*.mp3")
            audio_files = [AudioSegment.from_mp3(file) for file in files]

            # Merge the audio files
            merged = sum(audio_files)
            for i in glob.glob("*.mp3"):
                os.remove(i)
            
            merged.export("static/result.mp3", format="mp3")

            break
        else:
            time.sleep(1)
  
