import json
from pathlib import Path

from ina_flask.ina_lib.status import delete_status
from ina_flask.main import app
from loguru import logger
from pytest import fixture

youtube_video_test = "KO8CdJ4tVVk"
youtube_video_test_long = "tn-xAjjgVcs"


data_test = {
    "data": [["n", 0.0, 1.7], ["l", 1.7, 7.14], ["n", 7.14, 10.74]],
    "embed": "https://www.youtube.com/embed/KO8CdJ4tVVk",
    "lib": "audio_segmenter",
    "status_code": 200,
}


@fixture
def download_test_youtube():
    delete_status(youtube_video_test)
    delete_status(youtube_video_test_long)
    response = app.test_client().get("/api?url=www.youtube.com/watch?v=KO8CdJ4tVVk")


def test_first_page():
    response = app.test_client().get("/")
    assert response.status_code == 200


def test_api(download_test_youtube):
    response = app.test_client().get(
        f"/api?url=www.youtube.com/watch?v={youtube_video_test}"
    )
    data = response.data.decode("utf-8")
    logger.debug(data)

    # download
    if type(data) == dict:
        assert data["data"] == data_test
    # cache
    if type(data) == list:
        assert data == data_test


def test_status(download_test_youtube):
    response = app.test_client().get(f"/api/status/{youtube_video_test}")
    data = json.loads(response.data.decode("utf-8"))
    logger.debug(data)

    assert data["data"] == data_test["data"]


def test_video_too_long():
    response = app.test_client().get(
        f"/api?url=www.youtube.com/watch?v={youtube_video_test_long}"
    )
    data = response.data.decode("utf-8")
    logger.debug(data)
    assert json.loads(data) == {
        "duration_in_seconds": 37221,
        "status": "too long",
        "video": "https://www.youtube.com/watch?v=tn-xAjjgVcs",
    }


def test_stats():
    response = app.test_client().get(f"/api/stats")
    data = response.data.decode("utf-8")
    logger.debug(data)
    assert "total_requests" in json.loads(data).keys()
    assert "video_link_openings" in json.loads(data).keys()
