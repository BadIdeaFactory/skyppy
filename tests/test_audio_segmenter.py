# import os
# import sys
# from unittest import TestCase

# from ina_flask.ina_lib.audio_segmenter import AudioSegmenter
# from ina_flask.ina_lib.download_audio import DownloadAudio
# from loguru import logger

# file_path = "tests/audio/file_example_MP3_700KB.mp3"
# logger.info(os.getcwd())
# os.chdir("./tests/audio/")


# class TestAudioSegmenter(TestCase):
#     def setUp(self) -> None:
#         yt = DownloadAudio(file_path)
#         yt.download("https://www.youtube.com/watch?v=S9ui5JK4c8k")
#         self.output = AudioSegmenter(file_path)

#     def test_example(self):

#         self.assertEqual(self.output["status_code"], 200)

#     def tearDown(self):
#         try:
#             os.remove(file_path)
#         except:
#             pass


# if __name__ == "__main__":
#     test = TestAudioSegmenter()
#     test.setUp()
#     test.test_example()
#     test.tearDown()
