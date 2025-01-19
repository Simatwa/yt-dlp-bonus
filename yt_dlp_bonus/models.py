"""
Model for extracted video info
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, Literal


class ExtractedInfoFormatFragments(BaseModel):
    url: str
    duration: Optional[float] = None


class ExtractedInfoFormat(BaseModel):
    class DownloaderOptions(BaseModel):
        http_chunk_size: Optional[int] = 0

    format_id: str
    format_note: Optional[str] = None
    ext: str
    protocol: Optional[str] = None
    acodec: Optional[str] = None
    vcodec: str
    url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    rows: Optional[int] = None
    columns: Optional[int] = None
    fragments: Optional[list[ExtractedInfoFormatFragments]] = None
    audio_ext: Optional[str] = None
    video_ext: Optional[str] = None
    vbr: Optional[float] = None
    abr: Optional[float] = None
    tbr: Optional[Any] = None  # To be checked
    resolution: Optional[str] = None
    aspect_ratio: Optional[float] = None
    filesize_approx: Optional[int] = 0
    http_headers: dict[str, str] = {}
    format: Optional[str] = None
    audio_video_size: Optional[int] = 0
    downloader_options: Optional[DownloaderOptions] = DownloaderOptions()


class ExtractedInfoThumbnail(BaseModel):
    url: str
    preference: int
    id: Optional[int] = None


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
    duration: Optional[float] = None
    view_count: int
    average_rating: Optional[Any] = None
    age_limit: int
    webpage_url: str
    categories: Optional[list[str]] = []
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
    upload_date: Optional[str] = None
    timestamp: Optional[int] = None
    availability: Optional[Literal["public", "private"]] = None
    original_url: str
    webpage_url_basename: str
    webpage_url_domain: str
    extractor: str
    extractor_key: str
    playlist: Any = None
    playlist_index: Any = None
    display_id: Optional[str] = None
    fulltitle: Optional[str] = None
    duration_string: Optional[str] = None
    release_year: Optional[int] = None
    is_live: Optional[bool] = None
    was_live: Optional[bool] = None
    requested_subtitles: Any = None
    # has_drm: Any = Field(None, alias="_has_drm")
    epoch: Optional[int] = None
    requested_formats: Optional[list[ExtractedInfoRequestedFormats]] = None
    # Others
    format: Optional[str] = None
    format_id: Optional[str] = None
    ext: Optional[str] = None
    protocol: Optional[str] = None
    language: Optional[str] = None
    format_note: Optional[str] = None
    filesize_approx: Optional[int] = 0
    tbr: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    resolution: Optional[str] = None
    fps: Optional[int] = None
    dynamic_range: Optional[str] = None
    vcodec: Optional[str] = None
    vbr: Optional[float] = None
    stretched_ratio: Any = None
    aspect_ratio: Optional[float] = None
    acodec: Optional[str] = None
    abr: Optional[float] = None
    asr: Optional[float] = None
    audio_channels: Optional[int] = None


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
