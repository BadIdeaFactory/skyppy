from ina_flask.ina_lib.audio_segmenter import AudioSegmenter
from ina_flask.ina_lib.download_audio import DownloadAudio
from loguru import logger


# class TestAudioSegmenter(TestCase):
def test_AudioSegmenter():
    file_path = "./tests/audio/file_example_MP3_700KB.mp3"

    downloadAudio = DownloadAudio("./tests/audio/file_example_MP3_700KB.mp3", "test_id")

    logger.debug(downloadAudio.download("https://www.youtube.com/watch?v=JpvX-cTsEB0"))

    output = AudioSegmenter(file_path)

    logger.debug(output)

    assert output == {
        "lib": "audio_segmenter",
        "data": [["q", 0.0, 0.52], ["m", 0.52, 27.2]],
        "status_code": 200,
    }
