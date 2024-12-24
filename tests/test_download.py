import pytest
from pathlib import Path
from yt_dlp_bonus.main import Download, YoutubeDLBonus
from tests import video_url, curdir

yb = YoutubeDLBonus()
extracted_info = yb.extract_info_and_form_model(video_url)
filename_prefix = "TEST_"


@pytest.fixture
def download():
    return Download(
        yt=yb,
        working_directory=curdir.joinpath("assets"),
        filename_prefix=filename_prefix,
        clear_temps=True,
    )


@pytest.mark.parametrize(
    ["quality", "ext", "audio_ext", "bitrate", "retain_ext", "output_ext"],
    [
        #  ("360p", "webm", "m4a", None, True, "webm"), can't merge webm & m4a
        ("360p", "mp4", "m4a", None, True, "mp4"),
        ("240p", "mp4", "webm", None, False, "mp4"),
        ("360p", "webm", "webm", None, True, "webm"),
        ("medium", "mp4", "webm", "128k", False, "mp3"),
        ("medium", "webm", "webm", None, True, "webm"),
        ("low", "webm", "m4a", "192k", False, "mp3"),
        ("low", "webm", "m4a", None, True, "m4a"),
        ("medium", "mp4", "webm", None, True, "webm"),
        ("low", "mp4", "m4a", "192k", False, "mp3"),
        ("low", "mp4", "m4a", None, True, "m4a"),
    ],
)
def test_download_audio_and_video(
    download: Download, quality, ext, audio_ext, bitrate, retain_ext, output_ext
):
    info_format = yb.get_video_qualities_with_extension(
        extracted_info=extracted_info, ext=ext, audio_ext=audio_ext
    )
    saved_to: Path = download.run(
        title=extracted_info.title,
        qualities_format=info_format,
        quality=quality,
        bitrate=bitrate,
        retain_extension=retain_ext,
    )
    assert saved_to.name.startswith(filename_prefix)
    assert saved_to.exists()
    assert saved_to.is_file()
    assert saved_to.as_posix().endswith(output_ext)
    download.clear_temp_files(saved_to)
