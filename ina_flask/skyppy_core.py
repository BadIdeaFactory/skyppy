import uuid
import youtube_dl
import os
from ina_tools import segmentation_to_json
from inaSpeechSegmenter import Segmenter, seg2csv
from tool.check_video_lenght import CheckVideoLenght

class Segment:
    def __init__(self, posted):
        self.filename: str
        self.video_id: str
        self.posted = posted
        self.logging: str

    def my_hook(self, d):
        if d["status"] == "finished":
            print("Done downloading, now converting ...")

    def download(self):
        self.filename = str(uuid.uuid4()) + ".mp3"

        try:
            filename = str(uuid.uuid4()) + ".mp3"
            print(filename)
            ydl_opts = {
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

            # stop concurrent youtube download
            open("status.txt", "a").close()
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.posted["link_video"]])
            self.video_id = ydl.extract_info(self.posted["link_video"], download = False)["id"]
            os.remove("status.txt")
            self.logging = self.video_id

        except Exception as e:
            self.logging = str(e)

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

            output = {"embed": embed, "data": segmentation_output, "status_code": 200}

            self.logging = str(output)

            return output
        except Exception as e:
            self.logging = str(e)

            return {"embed": "error", "data": "error", "status_code": 404}
        finally:
            for item in os.listdir():
                if item[-3:] == "mp3":
                    os.remove(item)


class Skyppy_flask:
    @staticmethod
    def process(request, make_response, Segment, jsonify, Cache, video_lengt_in_minutes: int = 15):
        posted = {}
        posted["link_video"] = "https://" + request.args.get(
            "url", default="*", type=str
        )

        video_lenght = CheckVideoLenght().get(posted["link_video"])
        
        if video_lenght >= 60 * video_lengt_in_minutes:
            return make_response(jsonify({"video": posted["link_video"], "duration_in_seconds": video_lenght, "status": "too long"}))

        id_youtube_file = (
            request.args.get("url", default="*", type=str).split("?v=")[1] + ".json"
        )
        try:
            cache = Cache(id_youtube_file)

            if cache.check_log():
                return cache.data_from_log()

            if request.args.get("noprocess", default=False, type=bool):
                return jsonify(False)

            segment = Segment(posted)
            segment.download()
            video_segment = segment.segmenter()
            output = jsonify(video_segment)
            if video_segment["embed"] != "error":
                cache.save_from_log(video_segment["embed"], video_segment["data"])
            result = output, 200
        except:
            payload = jsonify(id_youtube_file)
            resp = make_response(payload, 404)
            result = resp
        return result
