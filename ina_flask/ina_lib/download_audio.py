import datetime
import json
import os
from random import randint

import youtube_dl
from ina_flask.ina_lib.status import Status


class DownloadAudio:
    """get Audio download"""

    def __init__(self, output_file, video_id):
        self.filename = output_file
        self.video_id = video_id

        self.ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": self.filename,
            "noplaylist": True,
            "progress_hooks": [self.my_hook],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

    def my_hook(self, d):
        if d["status"] == "finished":
            print("Done downloading, now converting ...")
        if d["status"] == "downloading":
            limit_status = randint(0, 100)
            if limit_status > 80:
                cur_status = Status(self.video_id)
                cur_status.current_download_percentage(d)

    def download(self, url: str) -> int:
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            result = ydl.download([url])
        return result


# if __name__ == "__main__":
#     # connection = DownloadAudio("./test/audio_test.mp3", "test_id")
#     # print(connection.download("https://www.youtube.com/watch?v=S9ui5JK4c8k"))
#     connection = DownloadAudio("./tests/audio/file_example_MP3_700KB.mp3", "test_id")
#     print(connection.download("https://www.youtube.com/watch?v=JpvX-cTsEB0"))
