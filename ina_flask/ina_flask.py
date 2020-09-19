from __future__ import unicode_literals
from flask import Flask, render_template, send_file, request, jsonify, make_response, url_for
from inaSpeechSegmenter import Segmenter, seg2csv
import pandas as pd
import re
import time
from ina_tools import segmentation_to_json
import json
from subprocess import call
import uuid
import youtube_dl
import os
#initialize flask
app = Flask(__name__)
app.static_url_path=app.config.get('video')
#create session object
session = {}

@app.route('/')
def first_page():
    return "api example = www.skyppy.io/api?url=www.youtube.com/watch?v={{youtube_id}}"


@app.route("/api", methods=["get"])
def api():
    posted = {}
    posted["link_video"] = "https://" + request.args.get('url', default='*', type=str)
    id_youtube_file = request.args.get('url', default='*', type=str).split("?v=")[1] + ".json"

    if id_youtube_file in os.listdir("./log"):
        with open("./log/" + id_youtube_file, "r") as youtube_in_memory:
            return json.load(youtube_in_memory)



    print(posted)
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    try:
        filename = str(uuid.uuid4()) + '.mp3'
        print(filename)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filename,
            'noplaylist': True,
            'progress_hooks': [my_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        # stop concurrent youtube download
        open("status.txt", 'a').close()
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([posted["link_video"]])
        video_id = ydl.extract_info(posted["link_video"])["id"]
        os.remove("status.txt")

        # initialize segmenter and use on-it
        seg = Segmenter()
        segmentation = seg(filename)
        segmentation_output = segmentation_to_json(segmentation)
        print(segmentation_output)
        session["segmentation_output"] = segmentation_output

        # set output youtube
        embed = "https://www.youtube.com/embed/{}".format(video_id)

        os.remove(filename)

        output = jsonify({
            "embed": embed,
            "data": segmentation_output}
            )



        with open("./log/" + id_youtube_file, "w") as logging_file:
            json.dump({"embed": embed, "data": segmentation_output}, logging_file)




        return output
    except Exception as e:
        
        return str(e)
    finally:
        for item in os.listdir():
            if item[-3:] == "mp3":
                os.remove(item)






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=False)

