"""Non-changing variables across the package"""

from enum import Enum
import typing as t


class VideoExtensions(Enum):
    """Video's extension i.e mp4 & webm"""

    mp4 = "mp4"
    webm = "webm"


videoQualities = t.Literal[
    "144p",
    "240p",
    "360p",
    "480p",
    "720p",
    "1080p",
    "1440p",
    "2160p",
    "720p50",
    "1080p50",
    "1440p50",
    "2160p50",
]
"""Video qualities"""

audioQualities = t.Literal[
    "ultralow",
    "low",
    "medium",
]
"""Audio qualities"""

mediaQualities = t.Literal[
    "ultralow",
    "low",
    "medium",
    "144p",
    "240p",
    "360p",
    "480p",
    "720p",
    "1080p",
    "1440p",
    "2160p",
    "720p50",
    "1080p50",
    "1440p50",
    "2160p50",
]
"""Both audio and video qualities"""
