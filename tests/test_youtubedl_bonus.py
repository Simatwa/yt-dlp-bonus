from yt_dlp_bonus.main import YoutubeDLBonus
from yt_dlp_bonus.models import ExtractedInfo
from tests import curdir

yb = YoutubeDLBonus()


def test_load_extracted_info_from_json_file():
    resp = yb.load_extracted_info_from_json_file(
        curdir / "assets/extracted-info-1.json"
    )
    assert isinstance(resp, ExtractedInfo)


def test_get_videos_quality_by_extension():
    resp = yb.load_extracted_info_from_json_file(
        curdir / "assets/extracted-info-1.json"
    )
    resp_1 = yb.get_videos_quality_by_extension(resp, "mp4")
    assert isinstance(resp_1, dict)
