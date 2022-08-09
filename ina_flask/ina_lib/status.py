import datetime
import json
import os
import uuid
from os.path import exists

server_id = str(uuid.uuid1())

from ina_lib import db

db.create_db()
db.init_db()


def check_status(youtube_id):
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
                "server_id": server_id,
            }


class Status:
    def __init__(self, youtube_id):
        self.youtube_id = youtube_id

    def too_long(self, video_lenght):
        data = {
            "video": self.youtube_id,
            "duration_in_seconds": video_lenght,
            "duration_in_minutes": video_lenght / 60,
            "status_description": "too long",
        }

        with db.DBSession() as session:
            new_status = db.DbStatus(youtube_id=self.youtube_id, data=data)
            session.merge(new_status)
            session.commit()
            return True

    def download(self):
        data = {
            "youtube_id": self.youtube_id,
            "status": 102,
            "status_description": "download",
            "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "server_id": server_id,
        }

        with db.DBSession() as session:
            new_status = db.DbStatus(youtube_id=self.youtube_id, data=data)
            session.merge(new_status)
            session.commit()
            return True

    def current_download_percentage(self, d):

        data = {
            "filename": d["filename"],
            "percent_str": d["_percent_str"],
            "eta_str": d["_eta_str"],
            "youtube_id": self.youtube_id,
            "status": 102,
            "status_description": "download",
            "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "server_id": server_id,
        }
        with db.DBSession() as session:
            new_status = db.DbStatus(youtube_id=self.youtube_id, data=data)
            session.merge(new_status)
            session.commit()
        # print(d["_percent_str"])
        print(" -- write to db")
        return True

    def segmenter(self):
        data = {
            "youtube_id": self.youtube_id,
            "status": 102,
            "status_description": "segmenter",
            "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "server_id": server_id,
        }
        with db.DBSession() as session:
            new_status = db.DbStatus(youtube_id=self.youtube_id, data=data)
            session.merge(new_status)
            session.commit()

    def complete(self, data):
        data = {
            "data": data,
            "youtube_id": self.youtube_id,
            "status": 200,
            "status_description": "complete",
            "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "server_id": server_id,
        }
        with db.DBSession() as session:
            new_status = db.DbStatus(youtube_id=self.youtube_id, data=data)
            session.merge(new_status)
            session.commit()
