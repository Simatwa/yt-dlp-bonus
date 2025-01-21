import pytest
from pathlib import Path
from yt_dlp_bonus.main import Download, YoutubeDLBonus
from tests import video_url, curdir

filename_prefix = "TEST_"
yb = YoutubeDLBonus(
    dict(
        outtmpl=f"{curdir}/temps/{filename_prefix}{Download.default_ydl_output_format}"
    )
)
extracted_info = yb.extract_info_and_form_model(video_url, filter_best_protocol=False)


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
        # ("360p", "webm", "m4a", None, True, "webm"), can't merge webm & m4a
        ("360p", "mp4", "m4a", None, True, "mp4"),
        ("240p", "mp4", "webm", None, False, "mp4"),
        ("360p", "webm", "webm", None, True, "webm"),
        ("medium", "mp4", "webm", "128k", False, "mp3"),
        ("medium", "webm", "webm", None, True, "webm"),
        ("medium", "webm", "webm", None, True, "webm"),
        ("medium", "webm", "m4a", "192k", False, "mp3"),
        ("medium", "webm", "m4a", None, True, "m4a"),
        # ("low", "mp4", "m4a", None, True, "m4a"),
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


@pytest.mark.parametrize(
    ["video_format", "audio_format", "default_format", "output_ext"],
    (
        ["240p", "m4a", None, None],
        ["240p", "m4a", None, "mkv"],
        ["240p", "medium", None, "mkv"],
        ["bestvideo[height=144]", None, None, None],
        ["bestvideo[height=144]", "m4a", None, "mp4"],
        ["bestvideo", "bestaudio", None, None],
        ["bestvideo", None, None, None],
        [None, "bestaudio", None, None],
        [None, None, "bestvideo+bestaudio[ext=m4a]", None],
        [None, None, "best", None],
    ),
)
def test_native_ydlp_run_download(
    download: Download, video_format: str, audio_format: str, default_format, output_ext
):
    info_dict = download.ydl_run(
        extracted_info,
        video_format=video_format,
        audio_format=audio_format,
        default_format=default_format,
        output_ext=output_ext,
    )
    assert isinstance(info_dict, dict)


@pytest.mark.parametrize(
    ["bitrate", "ext"],
    ([None, None], [None, "m4a"], ["128k", "m4a"], ["192k", "webm"], ["320k", None]),
)
def test_native_ytdlp_run_audio_download(
    download: Download, bitrate: str | None, ext: str | None
):
    format = f"bestaudio[ext={ext}]" if ext else "bestaudio"
    info_dict = download.ydl_run_audio(
        extracted_info, bitrate=bitrate, audio_format=format
    )
    assert type(info_dict) is dict


@pytest.mark.parametrize(
    ["video_format", "output_ext", "audio_ext"],
    (
        ["144p", "mp4", None],
        ["240p", "webm", "webm"],
        ["360p", "mp4", "m4a"],
        ["480p", "mkv", None],
    ),
)
def test_native_ytdlp_run_video_download(
    download: Download, video_format, output_ext, audio_ext
):
    audio_format = f"bestaudio[ext={audio_ext}]" if audio_ext else "bestaudio"
    info_dict = download.ydl_run_video(
        extracted_info,
        video_format=video_format,
        output_ext=output_ext,
        audio_format=audio_format,
    )

    assert type(info_dict) is dict


@pytest.mark.parametrize(
    ["audio_quality", "video_quality"],
    [
        ("medium", None),
        (None, "240p"),
        ("medium", "360p"),
    ],
)
def test_native_ytdlp_run_ids_download(
    download: Download, audio_quality: str, video_quality: str
):
    info_format = yb.get_video_qualities_with_extension(extracted_info=extracted_info)
    format_ids = []
    if audio_quality:
        format_ids.append(info_format[audio_quality].format_id)
    if video_quality:
        format_ids.append(info_format[video_quality].format_id)
    info_dict = download.ydl_run_ids(extracted_info, format_ids)
    assert type(info_dict) is dict
