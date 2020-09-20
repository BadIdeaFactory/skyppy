from __future__ import unicode_literals
import os
from flask import Flask, render_template, send_file, request, jsonify, make_response, url_for
from ina_cache import Cache
import pandas as pd
import re
import time
import json
from subprocess import call
from skyppy_core import Segment





#initialize flask
app = Flask(__name__)
app.static_url_path=app.config.get('video')




@app.route('/')
def first_page():
    return "api example = www.skyppy.io/api?url=www.youtube.com/watch?v={{youtube_id}}"

@app.route("/api", methods=["get"])
def api():
    posted = {}
    posted["link_video"] = "https://" + request.args.get('url', default='*', type=str)
    id_youtube_file = request.args.get('url', default='*', type=str).split("?v=")[1] + ".json"

    cache = Cache(id_youtube_file)

    if cache.check_log():
        return cache.data_from_log()

    segment = Segment(posted)
    segment.download()
    video_segment = segment.segmenter()
    output = jsonify(video_segment)
    if video_segment["embed"] != "error":
        cache.save_from_log(video_segment["embed"], video_segment["data"])
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5025, threaded=False)

