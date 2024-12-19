import pytest
from pathlib import Path
from yt_dlp_bonus.main import Download, YoutubeDLBonus
from yt_dlp_bonus.models import ExtractedInfo
from tests import video_url, curdir

yb = YoutubeDLBonus()
extracted_info = yb.extract_info_and_form_model(video_url)


@pytest.fixture
def download():
    return Download(
        yt=yb,
        working_directory=curdir.joinpath("assets"),
        file_prefix="TEST_",
        clear_temps=True,
    )


@pytest.mark.parametrize(
    ["quality", "extension", "bitrates", "audio_only"],
    [
        ("240p", "mp4", "128k", False),  # Download video in mp4
        ("360p", "webm", "128k", False),  # Download video in webm
        ("medium", "mp4", None, True),  # Download audio in m4a
        ("low", "webm", "192k", True),  # Download audio in mp3
    ],
)
def test_download_audio_and_video(
    download: Download, quality, extension, bitrates, audio_only
):
    info_format = yb.get_videos_quality_by_extension(
        extracted_info=extracted_info, ext=extension
    )
    saved_to: Path = download.run(
        title=extracted_info.title,
        quality_infoFormat=info_format,
        quality=quality,
        audio_bitrates=bitrates,
        audio_only=audio_only,
    )
    assert saved_to.exists()
    assert saved_to.is_file()
    download.clear_temp_files(saved_to)
