import datetime
import json
import os
import uuid
from os.path import exists

from ina_lib.status import Status

server_id = str(uuid.uuid1())

from ina_lib import db

db.create_db()
db.init_db()


class Cache:
    def __init__(self, id_youtube_file):
        self.id_youtube_file = id_youtube_file.split(".json")[0]

    def check_log(self):
        # if self.id_youtube_file in os.listdir("./log"):
        #     return True
        with db.DBSession() as session:
            youtube_exist = (
                session.query(db.DbStatus)
                .filter(db.DbStatus.youtube_id == self.id_youtube_file)
                .first()
            )
            if youtube_exist:
                if (
                    db.to_dict(youtube_exist)["data"]["status_description"]
                    == "complete"
                ):
                    return True

    def data_from_log(self):
        # with open("./log/" + self.id_youtube_file, "r") as youtube_in_memory:
        #     return json.load(youtube_in_memory)
        with db.DBSession() as session:
            youtube_exist = (
                session.query(db.DbStatus)
                .filter(db.DbStatus.youtube_id == self.id_youtube_file)
                .first()
            )
            if youtube_exist:
                return db.to_dict(youtube_exist)["data"]

    def save_from_log(self, embed, segmentation_output):
        if segmentation_output == "error":
            pass
        else:
            # with open("./log/" + self.id_youtube_file, "w") as logging_file:
            #     json.dump(
            #         {"cache": "True", "embed": embed, "data": segmentation_output},
            #         logging_file,
            #     )
            data = {
                "cache": "True",
                "data": segmentation_output,
                "embed": embed,
                "youtube_id": self.id_youtube_file,
                "status": 200,
                "status_description": "complete",
                "datetime": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                "server_id": server_id,
            }
        with db.DBSession() as session:
            new_status = db.DbStatus(youtube_id=self.id_youtube_file, data=data)
            session.merge(new_status)
            session.commit()
