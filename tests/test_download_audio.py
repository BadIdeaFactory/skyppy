# import os
# import sys
# from pathlib import Path
# from unittest import TestCase

# from ina_flask.ina_lib.download_audio import DownloadAudio
# from loguru import logger

# file_path = "./tests/audio/file_example_MP3_700KB.mp3"
# logger.info(os.getcwd())
# os.chdir("./tests/audio/")
# # file_path = os.path.join(os.getcwd(), file_path)

# # print(os.getcwd())
# # print(os.path.isfile(file_path))
# # print(os.listdir(os.getcwd()))


# class TestDownloadAudio(TestCase):
#     def setUp(self):
#         try:
#             os.remove(file_path)
#         except:
#             pass

#     def test_download_function(self):
#         print(os.listdir(os.getcwd()))
#         yt = DownloadAudio(file_path)
#         yt.download("https://www.youtube.com/watch?v=S9ui5JK4c8k")
#         self.assertTrue(os.path.isfile(file_path))

#     def tearDown(self):
#         try:
#             os.remove(file_path)
#         except:
#             pass


# if __name__ == "__main__":
#     test = TestDownloadAudio()
#     test.setUp()
#     test.test_download_function()
#     test.tearDown()
