import os
import sys
from unittest import TestCase

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))

from ina_lib.audio_segmenter import AudioSegmenter
from ina_lib.download_audio import DownloadAudio
file_path = "audio_test.mp3"
os.chdir("./test")

class TestAudioSegmenter(TestCase):
    def setUp(self) -> None:
        yt = DownloadAudio(file_path)
        yt.download("https://www.youtube.com/watch?v=S9ui5JK4c8k")
        self.output = AudioSegmenter(file_path)
        
    
    def test_example(self):
        
        self.assertEqual(self.output["status_code"], 200)
    
    def tearDown(self):
        try:
            os.remove(file_path)
        except:
            pass

if __name__ == "__main__":
    test = TestAudioSegmenter()
    test.setUp()
    test.test_example()
    test.tearDown()