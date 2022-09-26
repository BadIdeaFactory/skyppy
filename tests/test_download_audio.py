# import os
# import sys
# from pathlib import Path
# from unittest import TestCase

from ina_flask.ina_lib.download_audio import DownloadAudio
from loguru import logger


def test_DownloadAudio():
    file_path = "./tests/audio/file_example_MP3_700KB.mp3"

    downloadAudio = DownloadAudio("./tests/audio/file_example_MP3_700KB.mp3", "test_id")

    logger.debug(downloadAudio.download("https://www.youtube.com/watch?v=JpvX-cTsEB0"))
