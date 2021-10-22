import os
import sys
from unittest import TestCase

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))


from lib.download_audio import DownloadAudio
os.chdir("./test")
file_path = "audio_test.mp3"
file_path = os.path.join(os.getcwd(), file_path)

print(os.getcwd())
print(os.path.isfile(file_path))
print(os.listdir(os.getcwd()))

class TestDownloadAudio(TestCase):
    def setUp(self):
        try:
            os.remove(file_path)
        except:
            pass

    def test_download_function(self):
        print(os.listdir(os.getcwd()))
        yt = DownloadAudio(file_path)
        yt.download("https://www.youtube.com/watch?v=S9ui5JK4c8k")
        self.assertTrue(os.path.isfile(file_path))

    def tearDown(self):
        try:
            os.remove(file_path)
        except:
            pass



if __name__ == "__main__":
    test = TestDownloadAudio()
    test.setUp()
    test.test_download_function()
    test.tearDown()
