from yt_dlp_bonus.main import YoutubeDLBonus, qualityExtractedInfoType
from yt_dlp_bonus.models import ExtractedInfo
from tests import curdir
import pytest
from tests import curdir

video_url = "https://youtu.be/S3wsCRJVUyg?si=ojUwQ5uSiOAVcwEt"


@pytest.fixture
def yb():
    return YoutubeDLBonus(params=dict(cookiefile=curdir.joinpath("cookies.txt")))


def extract_info_from_json_file(yb: YoutubeDLBonus):
    return yb.load_extracted_info_from_json_file(
        curdir / "assets/extracted-info-1.json"
    )


def test_load_extracted_info_from_json_file(yb: YoutubeDLBonus):
    resp = extract_info_from_json_file(yb)
    assert isinstance(resp, ExtractedInfo)


def test_get_videos_quality_by_extension(yb: YoutubeDLBonus):
    extracted_data = extract_info_from_json_file(yb)
    resp_1 = yb.get_videos_quality_by_extension(extracted_data, "mp4")
    assert isinstance(resp_1, dict)


@pytest.mark.parametrize(["audio_quality"], [("ultralow",), ("low",), ("medium",)])
def test_update_audio_video_size(yb: YoutubeDLBonus, audio_quality):
    extracted_data = extract_info_from_json_file(yb)
    mp4_quality_formats = yb.get_videos_quality_by_extension(extracted_data, "mp4")
    resp = yb.update_audio_video_size(mp4_quality_formats, audio_quality)
    assert type(resp) in (qualityExtractedInfoType, dict)
    for quality, format in resp.items():
        assert isinstance(format.filesize_approx, int)
        assert isinstance(format.audio_video_size, int)
        assert format.audio_video_size >= format.filesize_approx


def test_extract_info_and_form_model(yb: YoutubeDLBonus):
    extracted_info = yb.extract_info_and_form_model(video_url)
    assert isinstance(extracted_info, ExtractedInfo)
