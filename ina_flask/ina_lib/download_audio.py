import datetime
import json
import os

import youtube_dl

from ina_lib.status import Status


def current_download_percentage(d, youtube_id):
    youtube_id_file = youtube_id + ".status"
    data = {
        "filename": d["filename"],
        "percent_str": d["_percent_str"],
        "eta_str": d["_eta_str"],
        "youtube_id": youtube_id,
        "status": 102,
        "status_description": "download",
        "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
    }
    print(data)

    with open(youtube_id_file, "w") as youtube_id_file_:
        youtube_id_file_.write(json.dumps(data))


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
            cur_status = Status(self.video_id)
            cur_status.current_download_percentage(d)

    def download(self, url: str) -> int:
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            result = ydl.download([url])
        return result


if __name__ == "__main__":
    connection = DownloadAudio("./test/audio_test.mp3", "test_id")
    print(connection.download("https://www.youtube.com/watch?v=S9ui5JK4c8k"))
