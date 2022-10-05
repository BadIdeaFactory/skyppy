import json

import pandas as pd
from ina_flask.ina_tools import segmentation_to_json, segmentation_to_pandas
from loguru import logger

test = [
    ("noEnergy", 0.0, 0.36),
    ("music", 0.36, 12.66),
    ("male", 12.66, 100.86),
    ("noEnergy", 100.86, 102.28),
    ("male", 102.28, 184.70000000000002),
    ("music", 184.70000000000002, 208.70000000000002),
    ("noEnergy", 208.70000000000002, 209.08),
]


def test_segmentation_to_pandas():
    data = segmentation_to_pandas(test)
    assert type(data) == pd.DataFrame
    assert data.iloc[0, -1] == 0.36
    assert data.iloc[-1, 0] == "noEnergy"


def test_segmentation_to_json():
    data = segmentation_to_json(test)
    assert type(data) == list
    assert data[0] == ["q", 0.0, 0.36]
    assert data[-1] == ["q", 208.7, 209.08]
