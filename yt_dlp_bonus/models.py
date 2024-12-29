"""
Model for extracted video info
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, Literal
from datetime import datetime


class ExtractedInfoFormatFragments(BaseModel):
    url: str
    duration: float


class ExtractedInfoFormat(BaseModel):
    class DownloaderOptions(BaseModel):
        http_chunk_size: Optional[int] = 0

    format_id: str
    format_note: Optional[str] = None
    ext: str
    protocol: str
    acodec: Optional[str] = None
    vcodec: str
    url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    rows: Optional[int] = None
    columns: Optional[int] = None
    fragments: Optional[list[ExtractedInfoFormatFragments]] = None
    audio_ext: str
    video_ext: str
    vbr: Optional[float] = None
    abr: Optional[float] = None
    tbr: Optional[Any] = None  # To be checked
    resolution: str
    aspect_ratio: Optional[float] = None
    filesize_approx: Optional[int] = 0
    http_headers: dict[str, str]
    format: str
    audio_video_size: Optional[int] = 0
    downloader_options: Optional[DownloaderOptions] = DownloaderOptions()


class ExtractedInfoThumbnail(BaseModel):
    url: str
    preference: int
    id: int


class ExtractedInfoAutomaticCaptions(BaseModel):
    ext: str
    url: str
    name: Optional[str] = None


class ExtractedInfoHeatmap(BaseModel):
    start_time: float
    end_time: float
    value: float


class ExtractedInfoRequestedFormats(ExtractedInfoFormat):
    asr: Any = None
    filesize: Optional[int] = 0
    source_preference: int
    audio_channels: Any = None
    quality: int
    has_drm: bool
    language: Optional[str] = None
    language_preference: Optional[int] = None
    preference: Any = None
    ext: str
    dynamic_range: Optional[str] = None
    container: Optional[str] = None
    downloader_options: Optional[dict[Any, Any]] = None


class ExtractedInfo(BaseModel):
    """Extracted video info"""

    id: str = Field(description="Youtube video ID")
    title: str = Field(description="Video title")
    formats: list[ExtractedInfoFormat]
    thumbnails: list[ExtractedInfoThumbnail]
    thumbnail: str
    description: str
    channel_id: str
    channel_url: str
    duration: float
    view_count: int
    average_rating: Optional[Any] = None
    age_limit: int
    webpage_url: str
    categories: list[str]
    tags: list[str]
    playable_in_embed: bool
    live_status: str
    release_timestamp: Optional[Any] = None
    # format_sort_fields: list[str] = Field(alias="_format_sort_fields")
    automatic_captions: dict[str, list[ExtractedInfoAutomaticCaptions]]
    subtitles: dict
    comment_count: Optional[int] = None
    chapters: Optional[Any] = None
    heatmap: Optional[list[ExtractedInfoHeatmap]] = None
    like_count: Optional[int] = None
    channel: str = Field(description="Channel name")
    channel_follower_count: int
    channel_is_verified: bool = False
    uploader: str
    uploader_id: Optional[str] = None
    uploader_url: Optional[str] = None
    upload_date: datetime
    timestamp: int
    availability: Literal["public", "private"]
    original_url: str
    webpage_url_basename: str
    webpage_url_domain: str
    extractor: str
    extractor_key: str
    playlist: Any = None
    playlist_index: Any = None
    display_id: str
    fulltitle: str = Field(description="Video title as it appears on YouTube")
    duration_string: str
    release_year: Optional[int] = None
    is_live: bool
    was_live: bool
    requested_subtitles: Any = None
    # has_drm: Any = Field(None, alias="_has_drm")
    epoch: int
    requested_formats: list[ExtractedInfoRequestedFormats]
    # Others
    format: str
    format_id: str
    ext: str
    protocol: str
    language: Optional[str] = None
    format_note: Optional[str] = None
    filesize_approx: Optional[int] = 0
    tbr: float
    width: int
    height: int
    resolution: str
    fps: int
    dynamic_range: Optional[str] = None
    vcodec: str
    vbr: float
    stretched_ratio: Any = None
    aspect_ratio: Optional[float] = None
    acodec: Optional[str] = None
    abr: float
    asr: float
    audio_channels: int


class SearchExtractedInfo(BaseModel):
    """Search results"""

    id: str
    title: str
    entries: list[ExtractedInfo]
    webpage_url: str
    original_url: str
    webpage_url_basename: str
    webpage_url_domain: Optional[str] = None
    extractor: str
    extractor_key: str
    release_year: Optional[Any] = None
    playlist_count: Optional[int] = 0
    epoch: int


class VideoFormats(BaseModel):
    webm: list[ExtractedInfoFormat]
    """Videos with .webm extensions"""
    mp4: list[ExtractedInfoFormat]
    """Videos with .mp4 extensions"""
