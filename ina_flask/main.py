from __future__ import unicode_literals

import json
import os
import re
import time
from subprocess import call

import pandas as pd
from flask import (
    Flask,
    Response,
    jsonify,
    make_response,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_cors import CORS
from loguru import logger

import ina_flask.config as config
from ina_flask.ina_lib.stats import get_statistics_of_video_link_openings
from ina_flask.ina_lib.status import check_status, statistics
from ina_flask.skyppy_core import Segment, Skyppy_flask

# initialize flask
app = Flask(__name__)
app.static_url_path = app.config.get("video")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/status/<youtube_id>")
def status(youtube_id):
    youtube_id_file_status = check_status(youtube_id)
    return jsonify(youtube_id_file_status)


@app.route("/guide")
def guide():
    return "api example = www.skyppy.tv/api?url=www.youtube.com/watch?v={{youtube_id}}"


@app.route("/api/stats")
def api_stats():
    return jsonify(get_statistics_of_video_link_openings())


@app.route("/pages/getStats", methods=["POST"])
def getStats():
    # flask get data from json request
    data = request.get_json()
    statistics(data["url"], data["youtube_id"])
    return jsonify({"data": data})


@app.route("/pages/stats")
def page_stats():
    data = get_statistics_of_video_link_openings()
    return render_template("stats.html", option=config.option.__dict__, data=data)


@app.route("/")
def first_page():

    return render_template("index.html", option=config.option.__dict__)


@app.route("/api", methods=["get", "post"])
def api():
    return Skyppy_flask.process(request, make_response, Segment, jsonify)


def start():
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host="0.0.0.0", port=8000, threaded=False)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host="0.0.0.0", port=8000, threaded=False)
