import os
import typer
import typing as t
from pathlib import Path
from yt_dlp_bonus.constants import videoQualities, audioQualities
from yt_dlp_bonus import YoutubeDLBonus, Downloader
from yt_dlp_bonus.models import ExtractedInfo
from enum import Enum

app = typer.Typer(help="Download Youtube videos in a number of formats.")

yt = YoutubeDLBonus()

downloader = Downloader(yt)

downloader.default_audio_extension_for_sorting = "webm"
downloader.default_video_extension_for_sorting = "webm"


def get_extracted_info(url: str) -> ExtractedInfo:
    resp = yt.extract_info_and_form_model(url)
    return resp


class VideoQualities(str, Enum):
    P144 = "144p"
    P240 = "240p"
    P360 = "360p"
    P480 = "480p"
    P720 = "720p"
    P1080 = "1080p"
    P1440 = "2k"
    P2160 = "4k"
    P4320 = "8k"
    BEST = "best"


class VideoExtensions(str, Enum):
    WEBM = "webm"
    MP4 = "mp4"


class AudioQualities(str, Enum):
    ULTRALOW = "ultralow"
    LOW = "low"
    MEDIUM = "medium"
    BESTAUDIO = "bestaudio"


class AudioBitrates(str, Enum):
    K64 = "64k"
    K96 = "96k"
    K128 = "128k"
    K192 = "192k"
    K256 = "256k"
    K320 = "320k"


@app.command()
def download_video(
    url: t.Annotated[str, typer.Argument(help="Link pointing to a Youtube video")],
    quality: t.Annotated[
        t.Optional[VideoQualities],
        typer.Option(help="Video quality to download", show_default=True),
    ] = VideoQualities.BEST,
    dir: t.Annotated[
        t.Optional[Path],
        typer.Option(
            help="Directory to save the video to",
            exists=True,
            writable=True,
            file_okay=False,
        ),
    ] = os.getcwd(),
    format: t.Annotated[
        t.Optional[VideoExtensions],
        typer.Option(help="Video format to process ie. mp4 or webm"),
    ] = VideoExtensions.WEBM,
    quiet: t.Annotated[
        t.Optional[bool],
        typer.Option(
            help="Do not stdout anything",
        ),
    ] = False,
    subtitle_lang: t.Annotated[
        t.Optional[str], typer.Option(help="Subtitle language to embed in the video")
    ] = None,
):
    """Download a youtube video"""
    extracted_info = get_extracted_info(url)
    downloader.default_video_extension_for_sorting = format
    qualities_videoFormat = yt.get_video_qualities_with_extension(
        extracted_info, ext=format.value
    )
    target_format = qualities_videoFormat.get(
        {"2k": "1440p", "4k": "2160p", "8k": "4320p"}.get(quality, quality)
    )
    if not quality == "best":
        assert target_format, (
            f"The video does not support that quality {quality}. Choose from "
            f"{', '.join([quality for quality in qualities_videoFormat.keys() if quality in videoQualities])}"
        )
    ytdl_params = {
        "quiet": quiet,
        "outtmpl": dir.joinpath(downloader.default_ydl_output_format).as_posix(),
    }
    if subtitle_lang:
        ytdl_params.update(
            {
                "postprocessors": [
                    {"already_have_subtitle": False, "key": "FFmpegEmbedSubtitle"}
                ],
                "writeautomaticsub": True,
                "writesubtitles": True,
                "subtitleslangs": [subtitle_lang],
            }
        )
    format = (
        "bestvideo+bestaudio"
        if format == "best"
        else f"{target_format.format_id}+{qualities_videoFormat["medium"].format_id}"
    )
    download_resp = downloader.ydl_run(
        extracted_info,
        video_format=None,
        audio_format=None,
        default_format=format,
        output_ext="mp4",
        ytdl_params=ytdl_params,
    )


@app.command()
def download_audio(
    url: t.Annotated[str, typer.Argument(help="Link pointing to a Youtube video")],
    quality: t.Annotated[
        t.Optional[AudioQualities],
        typer.Option(help="Video quality to download", show_default=True),
    ] = AudioQualities.BESTAUDIO,
    dir: t.Annotated[
        t.Optional[Path],
        typer.Option(
            help="Directory to save the video to",
            exists=True,
            writable=True,
            file_okay=False,
        ),
    ] = os.getcwd(),
    format: t.Annotated[
        t.Optional[VideoExtensions],
        typer.Option(help="Video format to process ie. mp4 or webm"),
    ] = VideoExtensions.WEBM,
    bitrate: t.Annotated[
        t.Optional[AudioBitrates],
        typer.Option(help="Audio bitrate while converting to mp3"),
    ] = None,
    quiet: t.Annotated[
        t.Optional[bool],
        typer.Option(help="Do not stdout anything"),
    ] = False,
):
    """Download audio version of a YouTube video"""
    extracted_info = get_extracted_info(url)
    downloader.default_video_extension_for_sorting = format
    qualities_videoFormat = yt.get_video_qualities_with_extension(
        extracted_info, ext=format.value
    )
    target_format = qualities_videoFormat.get(quality)
    if not quality == "bestaudio":
        assert target_format, (
            f"The video does not support that quality {quality}. "
            f"Choose from "
            f"{', '.join([quality for quality in qualities_videoFormat.keys() if quality in audioQualities])}"
        )
    format = "bestaudio" if quality == "bestaudio" else str(target_format.format_id)
    ytdl_params = {
        "quiet": quiet,
        "outtmpl": dir.joinpath(downloader.default_ydl_output_format).as_posix(),
    }
    download_resp = downloader.ydl_run_audio(
        extracted_info,
        bitrate=bitrate,
        audio_format=None,
        default_format=format,
        ytdl_params=ytdl_params,
    )


if __name__ == "__main__":
    app()
