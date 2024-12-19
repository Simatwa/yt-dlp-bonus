import json
import os
import time
import shutil
import typing as t
from uuid import uuid4
from pathlib import Path
from yt_dlp import YoutubeDL
from yt_dlp_bonus.models import ExtractedInfo, VideoFormats, ExtractedInfoFormat
from yt_dlp_bonus.constants import (
    VideoExtensions,
    videoQualities,
    audioQualities,
    mediaQualities,
    audioBitrates,
    audioQualitiesType,
    mediaQualitiesType,
    audioBitratesType,
)
from yt_dlp_bonus.utils import (
    logger,
    assert_instance,
    assert_type,
    assert_membership,
    get_size_in_mb_from_bytes,
    run_system_command,
)
from yt_dlp_bonus.exceptions import UserInputError

from yt_dlp.utils import sanitize_filename

qualityExtractedInfoType = dict[mediaQualitiesType, ExtractedInfoFormat]


class YoutubeDLBonus(YoutubeDL):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __enter__(self) -> "YoutubeDLBonus":
        return self

    def model_extracted_info(self, data: dict) -> ExtractedInfo:
        """Generate a model for the extracted video info.

        Args:
            data (dict): Extracted video info.

        Returns:
            ExtractedInfo: Modelled video info
        """
        extracted_data = ExtractedInfo(**data)
        sorted_formats = []
        for format in extracted_data.formats:
            format.downloader_options.http_chunk_size = format.filesize_approx
            sorted_formats.append(format)
        extracted_data.formats = sorted_formats
        return extracted_data

    def extract_info_and_form_model(self, url: str) -> ExtractedInfo:
        """Exract info for a particular url and model the response.

        Args:
            url (str): Youtube video url

        Returns:
            ExtractedInfo: Modelled video info
        """
        extracted_info = self.extract_info(url, download=False)
        return self.model_extracted_info(extracted_info)

    def load_extracted_info_from_json_file(
        self, to_json_path: Path | str
    ) -> ExtractedInfo:
        """Read extracted video info from .json and return it's modelled version

        Args:
            to_json_path (Path | str): Path to `.json` file containing the extracted video info.

        Returns:
            ExtractedInfo: Modelled video info.
        """
        with open(to_json_path) as fh:
            data = json.load(fh)
        return self.model_extracted_info(data)

    def separate_videos_by_extension(
        self, extracted_info: ExtractedInfo
    ) -> VideoFormats:
        """Separate videos available based on their extensions (webm, mp4)

        Args:
            extracted_info (ExtractedInfo): Modelled extracted video info.

        Returns:
            VideoFormats: Video separated into webm and mp4.
        """
        assert_instance(extracted_info, ExtractedInfo, "extracted_info")
        webm_videos: list = []
        mp4_videos: list = []

        for format in extracted_info.formats:
            if format.ext == VideoExtensions.webm:
                if format.format_note in audioQualities:
                    # Let's append audio to be accessible from both extensions
                    webm_videos.append(format)
                    mp4_videos.append(format)
                else:
                    webm_videos.append(format)
            elif format.ext == VideoExtensions.mp4:
                mp4_videos.append(format)

        return VideoFormats(webm=webm_videos, mp4=mp4_videos)

    def get_videos_quality_by_extension(
        self, extracted_info: ExtractedInfo, ext: t.Literal["webm", "mp4"] = "mp4"
    ) -> qualityExtractedInfoType:
        """Create a map of video qualities and their metadata.

        Args:
            extracted_info (ExtractedInfo): Extracted video info (modelled)
            ext (t.Literal["webm", "mp4"], optional): Video extensions. Defaults to "mp4".

        Returns:
            dict[mediaQualities,ExtractedInfoFormat]
        """
        separated_videos = self.separate_videos_by_extension(extracted_info)
        formats: list[ExtractedInfoFormat] = getattr(separated_videos, ext)
        response_items = {}
        for format in formats:
            if format.format_note and format.format_note in mediaQualities:
                response_items[format.format_note] = format

        return t.cast(qualityExtractedInfoType, response_items)

    def update_audio_video_size(
        self,
        quality_extracted_info: qualityExtractedInfoType,
        audio_quality: audioQualitiesType = "medium",
    ) -> qualityExtractedInfoType:
        """Takes the targeted audio size and adds it with that of each video.
        Updates the value to `filesize_approx` variable.

        Args:
            quality_extracted_info (qualityExtractedInfoType): Video qualities mapped to their ExtractedInfo.
            audio_quality (audioQualities): Audio qaulity from `ultralow`, `low`, `medium`.

        Returns:
            qualityExtractedInfoType: Updated qualityExtractedInfoType.
        """
        assert_type(
            quality_extracted_info,
            (qualityExtractedInfoType, dict),
            "quality_extracted_info",
        )
        assert_type(audio_quality, (audioQualitiesType, str), "audio_quality")
        chosen_audio_format = quality_extracted_info[audio_quality]
        for quality, format in quality_extracted_info.items():
            if quality in videoQualities:
                format.audio_video_size = (
                    format.filesize_approx + chosen_audio_format.filesize_approx
                )
            else:
                format.audio_video_size = format.filesize_approx
            quality_extracted_info[quality] = format

        return t.cast(qualityExtractedInfoType, quality_extracted_info)


class PostDownload:
    """Provides post download utilities"""

    merge_audio_and_video_command_template = (
        'ffmpeg -i "%(video_path)s" -i "%(audio_path)s" -c copy "%(output)s"'
    )
    audio_to_mp3_conversion_command_template = (
        'ffmpeg -i "%(input)s" -b:a %(bitrate)s "%(output)s"'
    )

    def __init__(self, clear_temps: bool = False):
        self.clear_temps: bool = clear_temps
        self.temp_dir: Path = None
        """Flag for controlling delition of temporary files"""

    def __enter__(self) -> "PostDownload":
        return self

    def clear_temp_files(self, *temp_files: Path | str):
        """Remove temporary files.

        Args:
            temp_files t.Sequence[Path|str]: temporary files.
        """
        if not self.clear_temps:
            logger.info(f"Ignoring temp-file clearance.")
            if self.temp_dir:
                for temp_file in temp_files:
                    try:
                        shutil.move(temp_file, self.temp_dir)
                    except Exception as e:
                        logger.error(
                            f"Error while moving temp_file '{temp_file}' to temp_dir '{self.temp_dir}' - {e} "
                        )
            return
        for temp_file in temp_files:
            logger.warning(f"Clearing temporary file - {temp_file}")
            try:
                os.remove(temp_file)
            except Exception as e:
                logger.exception(f"Failed to clear temp-file {temp_file}")

    def merge_audio_and_video(
        self, audio_path: Path, video_path: Path, output: Path | str
    ) -> Path:
        """Combines separate audio and video into one.

        Args:
            audio_path (Path): Path to audio file.
            video_path (Path): Path to video file.
            output (Path | str): Path to save the combined clips.

        Returns:
            Path: The clip path.

        ## Requires `ffmpeg` installed in system.
        """
        assert (
            audio_path.is_file()
        ), f"Audio file does not exists in path - {audio_path} "
        assert (
            video_path.is_file()
        ), f"Video file does not exists in path - {video_path}"
        assert not Path(
            str(output)
        ).is_dir(), f"Output path cannot be a directory - {output}"
        command = self.merge_audio_and_video_command_template % (
            dict(video_path=video_path, audio_path=audio_path, output=output)
        )
        logger.info(
            f"Merging audio and video - ({audio_path}, {video_path}) - {output}"
        )
        is_successful, resp = run_system_command(command)
        if not is_successful:
            raise RuntimeError("Failed to merge audio and video clips") from resp
        self.clear_temp_files(audio_path, video_path)
        return Path(str(output))

    def convert_audio_to_mp3_format(
        self, input: Path, output: Path | str, bitrate: audioBitratesType = "128k"
    ) -> Path:
        """Converts `.webm` and `.m4a` audio formats to `.mp3`.

        Args:
            input (Path): Path to audio file.
            output (Path | str): Path to save the mp3 file.
            bitrate (audioBitratesType, optional): Encoding bitrates. Defaults to "128k".

        Raises:
            RuntimeError: Incase conversion fails.

        Returns:
            Path: The clip path.
        """
        assert input.is_file(), f"Invalid value for input file - {input}"
        assert not Path(
            str(output)
        ).is_dir(), f"Output path cannot be a directory - {output}"
        assert_membership(audioBitrates, bitrate)
        command = self.audio_to_mp3_conversion_command_template % dict(
            input=input, bitrate=bitrate, output=output
        )
        logger.info(f"Converting audio file to mp3 - ({input}, {output})")
        is_successful, resp = run_system_command(command)
        if not is_successful:
            raise RuntimeError("Failed to convert audio to mp3") from resp
        self.clear_temp_files(input)
        return Path(str(output))


class Download(PostDownload):
    """Download audios and videos"""

    def __init__(
        self,
        yt: YoutubeDLBonus,
        working_directory: Path | str = os.getcwd(),
        clear_temps: bool = True,
        file_prefix: str = "",
        audio_quality: audioQualitiesType = "medium",
    ):
        """`Download` Constructor

        Args:
            working_directory (Path | str, optional): Diretory for saving files. Defaults to os.getcwd().
            clear_temps (bool, optional): Flag for clearing temporary files after download. Defaults to True.
            file_prefix (str, optional): Downloaded filename prefix. Defaults to "".
            audio_quality (str, audioQualitieType): One of ["ultralow", "low", "medium"]. Defaults to "medium".
        """
        super().__init__(clear_temps=clear_temps)
        self.yt = yt
        self.working_directory = Path(working_directory)
        self.clear_temps = clear_temps
        self.file_prefix = file_prefix
        self.audio_quality = audio_quality
        assert (
            self.working_directory.is_dir()
        ), f"Working directory chosen is invalid - {self.working_directory}"
        self.temp_dir = self.working_directory.joinpath("temps")
        os.makedirs(self.temp_dir, exist_ok=True)

    def __enter__(self) -> "Download":
        return self

    def save_to(self, title: str, ext: str = "", is_temp: bool = False) -> Path:
        """Get sanitized path to save a file

        Args:
            title (str): Video title.
            ext (str): File extension. defaults to "".
            is_temp (bool, optional): Flag for temporary file. Defaults to False.

        Returns:
            Path: Path of the file.
        """
        sanitized_filename = sanitize_filename(self.file_prefix + title)
        parent = self.temp_dir if is_temp else self.working_directory
        extension = ext if ext.startswith(".") else ("." + ext)
        return parent.joinpath(sanitized_filename + extension)

    def run(
        self,
        title: str,
        quality: mediaQualitiesType,
        quality_infoFormat: qualityExtractedInfoType,
        audio_bitrates: audioBitratesType = "128k",
        audio_only: bool = False,
    ) -> Path:
        """Download the media and save in disk.

        Args:
            title (str): Video title.
            quality_infoFormat (qualityExtractedInfoType): Qualities mapped to their `ExtractedInfoFormats`.
            quality (mediaQualitiesType): Quality of the media to be downloaded.
            audio_bitrates (audioBitratesType, optional): Audio encoding bitrates. Make it None to retains its's initial format. Defaults to "128k".
            audio_only (bool, optional): Flag to control video or audio download. Defaults to False.

        Returns:
              Path: Path to the downloaded file.
        """
        assert title, "Video title cannot be null"
        assert_membership(mediaQualities, quality)
        assert_membership(audioBitrates + (None,), audio_bitrates)
        assert_type(quality_infoFormat, (qualityExtractedInfoType, dict))
        assert (
            quality in quality_infoFormat
        ), f"The video does not support the targeted quality - {quality}"
        target_format = quality_infoFormat[quality]
        title = f"{title} {quality}"
        if quality in videoQualities and not audio_only:
            # Video being handled
            save_to = self.save_to(title, ext=target_format.ext)
            if save_to.exists():
                # let's presume it was previously processed.
                return save_to

            # Need to download both audio and video and then merge
            logger.info(
                f"Downloading video - {title} ({target_format.resolution}) [{get_size_in_mb_from_bytes(target_format.filesize_approx)}]"
            )
            # Let's download video
            video_temp = f"temp_{str(uuid4())}.{target_format.ext}"
            self.yt.dl(name=video_temp, info=target_format.model_dump())

            # Let's download audio
            target_audio_format = quality_infoFormat[self.audio_quality]
            logger.info(
                f"Downloading audio - {title} ({target_audio_format.resolution}) [{get_size_in_mb_from_bytes(target_audio_format.filesize_approx)}]"
            )
            audio_temp = f"temp_{str(uuid4())}.{target_audio_format.ext}"
            self.yt.dl(name=audio_temp, info=target_format.model_dump())

            self.merge_audio_and_video(
                audio_path=Path(audio_temp),
                video_path=Path(video_temp),
                output=save_to,
            )
        elif quality in audioQualities:
            # Download the desired audio quality
            title = f"{title} {audio_bitrates}" if audio_bitrates else title
            save_to = self.save_to(
                title, ext="mp3" if audio_bitrates else target_format.ext
            )
            if save_to.exists():
                # let's presume it was previously processed.
                return save_to
            logger.info(
                f"Downloading audio - {title} ({target_format.resolution}) [{get_size_in_mb_from_bytes(target_format.filesize_approx)}]"
            )
            audio_temp = f"temp_{str(uuid4())}.{target_format.ext}"
            self.yt.dl(name=audio_temp, info=target_format.model_dump())
            # Move audio to static
            if audio_bitrates:
                # Convert to mp3
                self.convert_audio_to_mp3_format(
                    input=Path(audio_temp), output=save_to, bitrate=audio_bitrates
                )
            else:
                # Retain in it's format
                # Move the file from tempfile to woking directory
                shutil.move(Path(audio_temp), save_to)
        else:
            raise UserInputError(
                f"The targeted format and quality mismatched - {quality}"
            )
        return save_to
