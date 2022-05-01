from __future__ import unicode_literals
import os
from flask import (
    Flask,
    render_template,
    send_file,
    request,
    jsonify,
    make_response,
    url_for,
    Response,
    render_template,
)
from flask_cors import CORS
from ina_lib.ina_cache import Cache
import pandas as pd
import re
import time
import json
from subprocess import call
from skyppy_core import Segment, Skyppy_flask
import config

# initialize flask
app = Flask(__name__)
app.static_url_path = app.config.get("video")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/status/<youtube_id>")
def status(youtube_id):
    with open(youtube_id + ".status", "r") as youtube_id_file_status:
        youtube_id_file_status = json.loads(youtube_id_file_status.read())

    return jsonify(youtube_id_file_status)


@app.route("/guide")
def guide():
    return "api example = www.skyppy.io/api?url=www.youtube.com/watch?v={{youtube_id}}"


@app.route("/")
def first_page():
    return render_template("index.html", option=config.option.__dict__)


@app.route("/api", methods=["get", "post"])
def api():
    return Skyppy_flask.process(request, make_response, Segment, jsonify, Cache)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7001, threaded=False)
