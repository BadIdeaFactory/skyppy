import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))


from inaSpeechSegmenter import Segmenter, seg2csv
from ina_tools import segmentation_to_json

def AudioSegmenter(input_file):
        # initialize segmenter and use on-it
        try:
            seg = Segmenter()
            segmentation = seg(input_file)
            segmentation_output = segmentation_to_json(segmentation)
            print(segmentation_output)

            output = {"lib": "audio_segmenter", "data": segmentation_output, "status_code": 200}


            return output
        except Exception as e:
            print(str(e))

            return {"lib": "audio_segmenter", "data": "error", "status_code": 404}


if __name__ == "__main__":
    print(AudioSegmenter("/app/test/audio_test.mp3"))