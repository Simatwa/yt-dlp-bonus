from yt_dlp_bonus.main import YoutubeDLBonus, qualityExtractedInfoType
from yt_dlp_bonus.models import ExtractedInfo
from tests import curdir
import pytest

yb = YoutubeDLBonus()


def extract_info_from_json_file():
    return yb.load_extracted_info_from_json_file(
        curdir / "assets/extracted-info-1.json"
    )


def test_load_extracted_info_from_json_file():
    resp = extract_info_from_json_file()
    assert isinstance(resp, ExtractedInfo)


def test_get_videos_quality_by_extension():
    extracted_data = extract_info_from_json_file()
    resp_1 = yb.get_videos_quality_by_extension(extracted_data, "mp4")
    assert isinstance(resp_1, dict)


@pytest.mark.parametrize(["audio_quality"], [("ultralow",), ("low",), ("medium",)])
def test_update_audio_video_size(audio_quality):
    extracted_data = extract_info_from_json_file()
    mp4_quality_formats = yb.get_videos_quality_by_extension(extracted_data, "mp4")
    resp = yb.update_audio_video_size(mp4_quality_formats, audio_quality)
    assert type(resp) in (qualityExtractedInfoType, dict)
