import uuid
import youtube_dl
import os
from ina_tools import segmentation_to_json
from inaSpeechSegmenter import Segmenter, seg2csv
from ina_lib.check_video_lenght import CheckVideoLenght
from ina_lib.download_audio import DownloadAudio
from ina_lib.audio_segmenter import AudioSegmenter
from ina_lib.get_video_id import get_video_id
from ina_lib.status import Status
class Segment:
    def __init__(self, posted):
        self.filename: str
        
        self.posted = posted
        self.logging: str
        self.input_file = str(uuid.uuid4()) + ".mp3"
        self.video_id = get_video_id(self.posted["link_video"])
        

    def my_hook(self, d):
        if d["status"] == "finished":
            print("Done downloading, now converting ...")

    def download(self):
    
        try:
            yt_connection = DownloadAudio(self.input_file)
            yt_connection.download(self.posted["link_video"])
        
        except Exception as e:
            self.logging = str(e)

        finally:
            pass

    def segmenter(self):
        # initialize segmenter and use on-it
        return AudioSegmenter(self.input_file)
            


class Skyppy_flask:
    @staticmethod
    def process(request, make_response, Segment, jsonify, Cache, video_lengt_in_minutes: int = 15):
        posted = {}
        posted["link_video"] = "https://" + request.args.get(
            "url", default="*", type=str
        )
        id_youtube_file = (
            request.args.get("url", default="*", type=str).split("?v=")[1] + ".json"
        )
        id_youtube = (
            request.args.get("url", default="*", type=str).split("?v=")[1]
        )
        
        try:
            video_lenght = CheckVideoLenght().get(posted["link_video"])
        except:
            payload = jsonify({"lib": "error: Video unavailable - wrong video url or your ip is banned from youtube", "data": "error", "status_code": 404})
            resp = make_response(payload, 404)
            result = resp
            return result
        
        if video_lenght >= 60 * video_lengt_in_minutes:
            result = make_response(jsonify({"video": posted["link_video"], "duration_in_seconds": video_lenght, "status": "too long"}))
            return result

        

        status = Status(id_youtube)
        try:
            cache = Cache(id_youtube_file)

            if cache.check_log():
                 result = cache.data_from_log()
                 return result

            # if request.args.get("noprocess", default=False, type=bool):
            #     return jsonify(False)

            segment = Segment(posted)
            try:
                if status.download():
                    segment.download()
                else:
                    payload = jsonify({"lib": """processing {id_youtube_file}""", "data": "please wait", "status_code": 102})
                    resp = make_response(payload, 102)
                    result = resp
                    return result

            except:
                payload = jsonify({"lib": "error_in_download", "data": "error", "status_code": 404})
                resp = make_response(payload, 404)
                result = resp
                return result
            status.segmenter()
            video_segment = segment.segmenter() 
            video_segment["embed"] = "https://www.youtube.com/embed/{}".format(segment.video_id)
            output = jsonify(video_segment)
            if video_segment["embed"] != "error":
                cache.save_from_log(video_segment["embed"], video_segment["data"])
            result = output, 200
            status.complete()
        except:
            payload = jsonify({"lib": "audio_segmenter", "data": "error", "status_code": 404})
            resp = make_response(payload, 404)
            result = resp

        finally:
            for item in os.listdir():
                if item[-3:] == "mp3":
                    os.remove(item)

            return result
