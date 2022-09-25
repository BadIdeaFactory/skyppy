import json
import os


class Cache:
    def __init__(self, id_youtube_file):
        self.id_youtube_file = id_youtube_file

    def check_log(self):
        if self.id_youtube_file in os.listdir("ina_flask/log"):
            return True

    def data_from_log(self):
        with open("ina_flask/log/" + self.id_youtube_file, "r") as youtube_in_memory:
            return json.load(youtube_in_memory)

    def save_from_log(self, embed, segmentation_output):
        if segmentation_output == "error":
            pass
        else:
            with open("ina_flask/log/" + self.id_youtube_file, "w") as logging_file:
                json.dump(
                    {"cache": "True", "embed": embed, "data": segmentation_output},
                    logging_file,
                )
