from yt_dlp_bonus.models import ExtractedInfo

import pytest

import json
from tests import curdir


@pytest.mark.parametrize(
    ["extracted_info_filename"],
    [
        ("assets/extracted-info.json",),
        ("assets/extracted-info-1.json",),
        ("assets/extracted-info-2.json",),
    ],
)
def test_extracted_info_modelling(extracted_info_filename):
    with open(curdir / extracted_info_filename) as fh:
        loaded_extracted_info = json.load(fh)
    ExtractedInfo(**loaded_extracted_info)
