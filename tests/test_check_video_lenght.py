from ina_flask.ina_lib.check_video_lenght import CheckVideoLenght


def test_CheckVideoLength():
    assert CheckVideoLenght().get("https://www.youtube.com/watch?v=H0Srb7Qv4Qc") == 181
