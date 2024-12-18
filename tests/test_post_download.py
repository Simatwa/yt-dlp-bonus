import pytest
from yt_dlp_bonus.main import PostDownload
from yt_dlp_bonus.constants import audioBitrates
from tests import curdir
import os

m4a_file_path = curdir.joinpath("assets/blob/videoplayback.m4a")
webm_file_path = curdir.joinpath("assets/blob/videoplayback.webm")
mp4_file_path = curdir.joinpath("assets/blob/videoplayback.mp4")


@pytest.fixture
def pd():
    ps = PostDownload()
    ps.clear_temps = False
    return ps


@pytest.mark.parametrize(
    ["audio_path", "video_path", "output"],
    [
        (m4a_file_path, mp4_file_path, curdir.joinpath("assets/m4a_mp4.mp4")),
        (webm_file_path, mp4_file_path, curdir.joinpath("assets/webm_mp4.mp4")),
    ],
)
def test_merge_audio_and_video(pd: PostDownload, audio_path, video_path, output):
    saved_to = pd.merge_audio_and_video(
        audio_path=audio_path,
        video_path=video_path,
        output=output,
    )
    assert saved_to.exists()
    assert saved_to.is_file()
    os.remove(saved_to)


@pytest.mark.parametrize(
    ["input", "output"],
    [
        (m4a_file_path, curdir.joinpath("assets/blob/m4a_mp3.mp3")),
        (webm_file_path, curdir.joinpath("assets/blob/webm_mp3.mp3")),
    ],
)
def test_audio_conversion_to_mp3(pd: PostDownload, input, output):
    for bitrate in audioBitrates:
        saved_to = pd.convert_audio_to_mp3_format(
            input=input,
            output=output,
            bitrate=bitrate,
        )
        assert saved_to.exists()
        assert saved_to.is_file()
        os.remove(saved_to)
