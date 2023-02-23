import os
import uuid
from typing import Dict

import youtube_dl
from flask import Response, jsonify, make_response
from inaSpeechSegmenter import Segmenter, seg2csv
from loguru import logger

import ina_flask.config as config
from ina_flask.ina_lib.audio_segmenter import AudioSegmenter
from ina_flask.ina_lib.check_video_lenght import CheckVideoLenght
from ina_flask.ina_lib.download_audio import DownloadAudio
from ina_flask.ina_lib.get_video_id import get_video_id, get_youtube_id_from_request
from ina_flask.ina_lib.status import Status, check_status, statistics
from ina_flask.ina_tools import segmentation_to_json


def if_video_too_long(
    video_lenght: int,
    video_lengt_in_minutes: int,
    posted: Dict,
    status: Status,
    make_response: make_response,
    jsonify,
) -> "Response":
    if video_lenght >= 60 * video_lengt_in_minutes:
        response = make_response(
            jsonify(
                {
                    "video": posted["link_video"],
                    "duration_in_seconds": video_lenght,
                    "status": "too long",
                }
            )
        )
        status.too_long(video_lenght)
        logger.info(f"status too long")
        return response


def if_video_doesnt_exist(
    video_lenght: int,
    video_lengt_in_minutes: int,
    posted: Dict,
    status: Status,
    make_response: make_response,
    jsonify,
) -> "Response":
    if video_lenght == 0:
        response = make_response(
            jsonify(
                {
                    "video": posted["link_video"],
                    "duration_in_seconds": video_lenght,
                    "status": "video does not exist",
                }
            )
        )
        status.doesnt_exist(video_lenght)
        logger.info(f"video does not exist")
        return response


def if_cache_exist(posted) -> "Response":
    cache = check_status(posted["id_youtube"])
    if "data" in cache.keys():
        # logger.info(
        #     statistics(
        #         url=posted["link_video"], youtube_dl=posted["id_youtube"]
        #     ).__dict__
        # )
        response = cache["data"]
        return response


def if_segmenter(status, segment):
    status.segmenter()
    video_segment = segment.segmenter()
    video_segment["embed"] = "https://www.youtube.com/embed/{}".format(segment.video_id)
    output = jsonify(video_segment)
    # if video_segment["embed"] != "error":
    #     cache.save_from_log(video_segment["embed"], video_segment["data"])
    response = output, 200
    status.complete(video_segment["data"])
    return response


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

        yt_connection = DownloadAudio(self.input_file, self.video_id)
        yt_connection.download(self.posted["link_video"])

        return yt_connection

    def segmenter(self):
        # initialize segmenter and use on-it
        return AudioSegmenter(self.input_file)


class Skyppy_flask:
    @staticmethod
    def process(
        request,
        make_response,
        Segment,
        jsonify,
        video_length_in_minutes: int = config.option.max_video_lenght_in_minutes,
    ):
        posted = get_youtube_id_from_request(request)
        logger.debug(f"get_youtube_id: {posted}")

        logger.debug("check video Lenght")
        status = Status(posted["id_youtube"])

        video_length = CheckVideoLenght().get(posted["link_video"])

        logger.debug(f"check if video doesn´t exist: {video_length}")
        if video_length == 0:

            not_exist = if_video_doesnt_exist(
                video_length,
                video_length_in_minutes,
                posted,
                status,
                make_response,
                jsonify,
            )
            logger.debug(not_exist)
            if not_exist:
                return not_exist

        # video too long
        too_long = if_video_too_long(
            video_length,
            video_length_in_minutes,
            posted,
            status,
            make_response,
            jsonify,
        )
        if too_long:
            return too_long

        logger.debug("check cache")

        # cache
        cache = if_cache_exist(posted)
        if cache:
            return cache

        logger.debug("start download")
        segment = Segment(posted)

        # download status
        status.download()
        # logger.info(
        #     statistics(
        #         url=posted["link_video"], youtube_dl=posted["id_youtube"]
        #     ).__dict__
        # )
        result = segment.download()
        logger.debug(f"finish download: {result}")

        # segmenting
        response = if_segmenter(status, segment)

        for item in os.listdir():
            if item[-3:] == "mp3":
                os.remove(item)

        return response
