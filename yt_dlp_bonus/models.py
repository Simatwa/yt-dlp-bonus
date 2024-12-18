"""
Model for extracted video info
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Any, Literal
from datetime import datetime


class ExtractedInfoFormatFragments(BaseModel):
    url: HttpUrl
    duration: float


class ExtractedInfoFormat(BaseModel):
    format_id: str
    format_note: str
    ext: str
    protocol: str
    acodec: str
    vcodec: str
    url: Optional[HttpUrl] = None
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
    filesize_approx: Optional[int] = None
    http_headers: dict[str, str]
    format: str
    audio_video_size: Optional[int] = 0


class ExtractedInfoThumbnail(BaseModel):
    url: HttpUrl
    preference: int
    id: int


class ExtractedInfoAutomaticCaptions(BaseModel):
    ext: str
    url: HttpUrl
    name: str


class ExtractedInfoHeatmap(BaseModel):
    start_time: float
    end_time: float
    value: float


class ExtractedInfoRequestedFormats(ExtractedInfoFormat):
    asr: Any = None
    filesize: int
    source_preference: int
    audio_channels: Any = None
    quality: int
    has_drm: bool
    language: Optional[str] = None
    language_preference: int
    preference: Any = None
    ext: str
    dynamic_range: Optional[str] = None
    container: str
    downloader_options: dict[Any, Any]


class ExtractedInfo(BaseModel):
    """Extracted video info"""

    id: str = Field(description="Youtube video ID")
    title: str = Field(description="Video title")
    formats: list[ExtractedInfoFormat]
    thumbnails: list[ExtractedInfoThumbnail]
    thumbnail: HttpUrl
    description: str
    channel_id: str
    channel_url: HttpUrl
    duration: float
    view_count: int
    average_rating: Optional[Any] = None
    age_limit: int
    webpage_url: HttpUrl
    categories: list[str]
    tags: list[str]
    playable_in_embed: bool
    live_status: str
    release_timestamp: Optional[Any] = None
    format_sort_fields: list[str] = Field(alias="_format_sort_fields")
    automatic_captions: dict[str, list[ExtractedInfoAutomaticCaptions]]
    subtitles: dict
    comment_count: Optional[int] = None
    chapters: Optional[Any] = None
    heatmap: Optional[list[ExtractedInfoHeatmap]] = None
    like_count: int
    channel: str = Field(description="Channel name")
    channel_follower_count: int
    channel_is_verified: bool = False
    uploader: str
    uploader_id: str
    uploader_url: HttpUrl
    upload_date: datetime
    timestamp: int
    availability: Literal["public", "private"]
    original_url: HttpUrl
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
    has_drm: Any = Field(None, alias="_has_drm")
    epoch: int
    requested_formats: list[ExtractedInfoRequestedFormats]
    # Others
    format: str
    format_id: str
    ext: str
    protocol: str
    language: Optional[str]
    format_note: str
    filesize_approx: int
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
    acodec: str
    abr: float
    asr: float
    audio_channels: int


class VideoFormats(BaseModel):
    webm: list[ExtractedInfoFormat]
    """Videos with .webm extensions"""
    mp4: list[ExtractedInfoFormat]
    """Videos with .mp4 extensions"""
