from yt_dlp_bonus.main import YoutubeDLBonus, qualityExtractedInfoType
from yt_dlp_bonus.models import ExtractedInfo, SearchExtractedInfo
from yt_dlp_bonus.constants import mediaQualities
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


def test_download_url_ip_address_update(yb: YoutubeDLBonus):
    download_ip_addr = "127.0.0.1"
    yb = YoutubeDLBonus(download_ip=download_ip_addr)
    extracted_info = extract_info_from_json_file(yb)
    for format in extracted_info.formats:
        if format.format_note in mediaQualities:
            assert "ip=127.0.0.1" in format.url


@pytest.mark.parametrize(
    ["extension", "audio_ext"],
    [
        ("mp4", "webm"),
        ("mp4", "m4a"),
        ("webm", "webm"),
        ("webm", "m4a"),
    ],
)
def test_get_video_qualities_with_extension(yb: YoutubeDLBonus, extension, audio_ext):
    extracted_data = extract_info_from_json_file(yb)
    resp_1 = yb.get_video_qualities_with_extension(extracted_data, extension, audio_ext)
    assert isinstance(resp_1, dict)
    assert resp_1.get("medium").ext == audio_ext


@pytest.mark.parametrize(["audio_quality"], [("ultralow",), ("low",), ("medium",)])
def test_update_audio_video_size(yb: YoutubeDLBonus, audio_quality):
    extracted_data = extract_info_from_json_file(yb)
    mp4_quality_formats = yb.get_video_qualities_with_extension(extracted_data, "mp4")
    resp = yb.update_audio_video_size(mp4_quality_formats, audio_quality)
    assert type(resp) in (qualityExtractedInfoType, dict)
    for quality, format in resp.items():
        assert isinstance(format.filesize_approx, int)
        assert isinstance(format.audio_video_size, int)
        assert format.audio_video_size >= format.filesize_approx


def test_extract_info_and_form_model(yb: YoutubeDLBonus):
    extracted_info = yb.extract_info_and_form_model(video_url)
    assert isinstance(extracted_info, ExtractedInfo)


@pytest.mark.parametrize(
    ["query", "limit", "filter_best_protocol"], [("hey", 1, True), ("hello", 2, False)]
)
def test_search_and_form_model(yb: YoutubeDLBonus, query, limit, filter_best_protocol):
    search_results = yb.search_and_form_model(query, limit, filter_best_protocol)
    assert isinstance(search_results, SearchExtractedInfo)
