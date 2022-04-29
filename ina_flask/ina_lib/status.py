import os
import json
import datetime

class Status:
    def __init__(self, youtube_id):
        self.youtube_id = youtube_id
        self.youtube_id_file = self.youtube_id + ".status"

    def download(self):
        if os.path.isfile(self.youtube_id_file):
            return False
        with open(self.youtube_id_file, "w") as youtube_id_file:
            youtube_id_file.write(json.dumps({"youtube_id": self.youtube_id, "status": 102, "status_description": "download", "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}))
        return True

    def current_download_percentage(self, d):

        data = {'filename': d['filename'],'percent_str':  d['percent_str'],'eta_str': d['_eta_str'],
            "youtube_id": self.youtube_id, "status": 102, "status_description": "download", "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
        with open(self.youtube_id_file, "w") as youtube_id_file:
            youtube_id_file.write(json.dumps(data))
        return True
    def segmenter(self):
        with open(self.youtube_id_file, "w") as youtube_id_file:
                youtube_id_file.write(json.dumps({"youtube_id": self.youtube_id, "status": 102, "status_description": "segmenter", "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}))

    def complete(self, data):
        with open(self.youtube_id_file, "w") as youtube_id_file:
                youtube_id_file.write(json.dumps({"data": data, "youtube_id": self.youtube_id, "status": 200, "status_description": "complete", "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}))
