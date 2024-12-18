from yt_dlp import YoutubeDL
from yt_dlp_bonus.models import ExtractedInfo, VideoFormats, ExtractedInfoFormat
from pathlib import Path
import json
from yt_dlp_bonus.constants import (
    VideoExtensions,
    audioQualities,
    audioQualitiesType,
    mediaQualitiesType,
)
from yt_dlp_bonus.utils import assert_instance, assert_type
import typing as t

qualityExtractedInfoType = dict[mediaQualitiesType, ExtractedInfoFormat]


class YoutubeDLBonus(YoutubeDL):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def model_extracted_info(self, data: dict) -> ExtractedInfo:
        """Generate a model for the extracted video info.

        Args:
            data (dict): Extracted video info.

        Returns:
            ExtractedInfo: Modelled video info
        """
        return ExtractedInfo(**data)

    def extract_info_and_model(self, url: str) -> ExtractedInfo:
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
            format.audio_video_size = (
                format.filesize_approx + chosen_audio_format.filesize_approx
            )
            quality_extracted_info[quality] = format
        return t.cast(qualityExtractedInfoType, quality_extracted_info)
