import uuid
import youtube_dl
from ina_tools import segmentation_to_json
from inaSpeechSegmenter import Segmenter, seg2csv
import os
from logger import inaLogger


class Segment:
    def __init__(self, posted):
        self.filename: str
        self.video_id: str
        self.posted = posted
        self.logging: str
        

    def my_hook(self,d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    def download(self):
        self.filename = str(uuid.uuid4()) + '.mp3'

        try:
            filename = str(uuid.uuid4()) + '.mp3'
            print(filename)
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': self.filename,
                'noplaylist': True,
                'progress_hooks': [self.my_hook],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            # stop concurrent youtube download
            open("status.txt", 'a').close()
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.posted["link_video"]])
            self.video_id = ydl.extract_info(self.posted["link_video"])["id"]
            os.remove("status.txt")
            self.logging = self.video_id
            inaLogger.write_to_log(self.logging)
        except Exception as e:
            self.logging = str(e)
            inaLogger.write_to_log(self.logging)
            return str(e)

        
    
    def segmenter(self):
        # initialize segmenter and use on-it
        try:
            seg = Segmenter()
            segmentation = seg(self.filename)
            segmentation_output = segmentation_to_json(segmentation)
            print(segmentation_output)
            

            # set output youtube
            embed = "https://www.youtube.com/embed/{}".format(self.video_id)

            os.remove(self.filename)

            output = {
                "embed": embed,
                "data": segmentation_output
                }
            
            self.logging = str(output)
            inaLogger.write_to_log(self.logging)
            return output
        except Exception as e:
            self.logging = str(e)
            inaLogger.write_to_log(self.logging)
            
            return { 
                "embed": "error",
                "data": "error"
                }
        finally:
            for item in os.listdir():
                if item[-3:] == "mp3":
                    os.remove(item)

            