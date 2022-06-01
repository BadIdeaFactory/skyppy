import datetime
import json
import os
from os.path import exists

from ina_lib import db

db.create_db()
db.init_db()


def check_status(youtube_id):
    filename = f"{youtube_id}.status"
    file_exists = exists(filename)
    with db.DBSession() as session:
        youtube_exist = (
            session.query(db.DbStatus)
            .filter(db.DbStatus.youtube_id == youtube_id)
            .first()
        )
        if youtube_exist:
            return db.to_dict(youtube_exist)["data"]
        else:
            return {
                "status_description": "not started",
                "message": f"{youtube_id} is not started",
            }


class Status:
    def __init__(self, youtube_id):
        self.youtube_id = youtube_id
        self.youtube_id_file = self.youtube_id + ".status"

    def download(self):
        data = json.dumps(
            {
                "youtube_id": self.youtube_id,
                "status": 102,
                "status_description": "download",
                "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            }
        )

        with db.DBSession() as session:
            new_status = db.DbStatus(youtube_id=self.youtube_id, data=data)
            session.merge(new_status)
            session.commit()
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
