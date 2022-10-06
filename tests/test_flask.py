import json

from ina_flask.main import app
from loguru import logger


def test_first_page():
    response = app.test_client().get("/")
    assert response.status_code == 200


def test_api():
    response = app.test_client().get("/api?url=www.youtube.com/watch?v=KO8CdJ4tVVk")
    data = response.data.decode("utf-8")
    logger.debug(data)

    data_test = {
        "data": [["n", 0.0, 1.72], ["l", 1.72, 7.04], ["n", 7.04, 10.74]],
        "embed": "https://www.youtube.com/embed/KO8CdJ4tVVk",
        "lib": "audio_segmenter",
        "status_code": 200,
    }

    # download
    if type(data) == dict:
        assert data["data"] == data_test
    # cache
    if type(data) == list:
        assert data == data_test
