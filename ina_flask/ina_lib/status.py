import datetime
import json
import os
from os.path import exists

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
            }


class Status:
    def __init__(self, youtube_id):
        self.youtube_id = youtube_id

    def download(self):
        data = {
            "youtube_id": self.youtube_id,
            "status": 102,
            "status_description": "download",
            "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
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
        }
        with db.DBSession() as session:
            new_status = db.DbStatus(youtube_id=self.youtube_id, data=data)
            session.merge(new_status)
            session.commit()

        print("write to db")
        return True

    def segmenter(self):
        data = {
            "youtube_id": self.youtube_id,
            "status": 102,
            "status_description": "segmenter",
            "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
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
        }
        with db.DBSession() as session:
            new_status = db.DbStatus(youtube_id=self.youtube_id, data=data)
            session.merge(new_status)
            session.commit()
