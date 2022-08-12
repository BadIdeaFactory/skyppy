import pandas as pd
from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS

import config
from ina_lib.status import Cache, check_status
from skyppy_core import Segment, Skyppy_flask

# initialize flask
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/status/<youtube_id>")
def status(youtube_id):
    """this route give the response with the status of processing of specific youtube_id (download, segmenting, complete)

    args:
        youtube_id (str)

    return:
        flask json response (str)

    """
    youtube_id_file_status = check_status(youtube_id)
    return jsonify(youtube_id_file_status)


@app.route("/guide")
def guide():
    return "api example = www.skyppy.io/api?url=www.youtube.com/watch?v={{youtube_id}}"


@app.route("/")
def first_page():
    """this route start homepage with preconfigured settings.

    Options can be modified in ./ina_flask/config.yaml:
        server_url (str): "/" -> server URL for Skyppy
        max_video_length_in_minutes (int): 15 -> max accepted video length (in minutes)
        deploy: "WEB" -> "WEB"/ "LOCALMACHINE"
            1. "LOCALMACHINE": use preconfigured local sqlite database
            2. "WEB": use remote mysql server
            in "WEB" in that case you need to create a ./ina_flask/web_deploy.py file and include a valid engine.URL as the sqlURL variable (sqlachemy).
    """

    option = {
        "server_url": config.option.server_url,
        "max_video_length_in_minutes": config.option.max_video_length_in_minutes,
    }
    return render_template("index.html", option=option)


@app.route("/api", methods=["get", "post"])
def api():
    """this route are the ones responsible of downloading the actual youtube file, analyze with inaspeech and return audio segmenter json

    return:
        json with audio segmentation in data key
    """
    return Skyppy_flask.process(request, make_response, Segment, jsonify, Cache)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7001, threaded=False)
