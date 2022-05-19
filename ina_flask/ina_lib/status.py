import datetime
import json
import os
from os.path import exists


def check_status(youtube_id):
    filename = f"{youtube_id}.status"
    file_exists = exists(filename)
    if file_exists:
        with open(filename, "r") as youtube_id_file_status:
            youtube_id_file_status = json.loads(youtube_id_file_status.read())
        return youtube_id_file_status
    else:
        return {
            "status_description": "not started",
            "message": f"{youtube_id} is not started {filename}",
        }


class Status:
    def __init__(self, youtube_id):
        self.youtube_id = youtube_id
        self.youtube_id_file = self.youtube_id + ".status"

    def download(self):
        if os.path.isfile(self.youtube_id_file):
            return False
        with open(self.youtube_id_file, "w") as youtube_id_file:
            youtube_id_file.write(
                json.dumps(
                    {
                        "youtube_id": self.youtube_id,
                        "status": 102,
                        "status_description": "download",
                        "datetime": datetime.datetime.now().strftime(
                            "%m/%d/%Y, %H:%M:%S"
                        ),
                    }
                )
            )
        return True

    def current_download_percentage(self, d):

        data = {
            "filename": d["filename"],
            "percent_str": d["percent_str"],
            "eta_str": d["_eta_str"],
            "youtube_id": self.youtube_id,
            "status": 102,
            "status_description": "download",
            "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        }
        with open(self.youtube_id_file, "w") as youtube_id_file:
            youtube_id_file.write(json.dumps(data))
        return True

    def segmenter(self):
        with open(self.youtube_id_file, "w") as youtube_id_file:
            youtube_id_file.write(
                json.dumps(
                    {
                        "youtube_id": self.youtube_id,
                        "status": 102,
                        "status_description": "segmenter",
                        "datetime": datetime.datetime.now().strftime(
                            "%m/%d/%Y, %H:%M:%S"
                        ),
                    }
                )
            )

    def complete(self, data):
        with open(self.youtube_id_file, "w") as youtube_id_file:
            youtube_id_file.write(
                json.dumps(
                    {
                        "data": data,
                        "youtube_id": self.youtube_id,
                        "status": 200,
                        "status_description": "complete",
                        "datetime": datetime.datetime.now().strftime(
                            "%m/%d/%Y, %H:%M:%S"
                        ),
                    }
                )
            )
