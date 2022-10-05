from ina_flask.ina_lib.get_video_id import get_video_id


def test_get_video_id():
    assert get_video_id("https://www.youtube.com/watch?v=OG__SwkV3wg") == "OG__SwkV3wg"
