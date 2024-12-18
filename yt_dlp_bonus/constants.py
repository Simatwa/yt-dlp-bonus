"""Non-changing variables across the package"""

import typing as t


class VideoExtensions:
    """Video's extension i.e mp4 & webm"""

    mp4 = "mp4"
    webm = "webm"


videoQualities = (
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
    "720p60",
    "1080p60",
    "1440p60",
    "2160p60",
)
"""Video qualities"""

videoQualitiesType = t.Literal[
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
    "720p60",
    "1080p60",
    "1440p60",
    "2160p60",
]

audioQualitiesType = t.Literal[
    "ultralow",
    "low",
    "medium",
]

audioQualities = (
    "ultralow",
    "low",
    "medium",
)
"""Audio qualities"""

mediaQualitiesType = t.Literal[
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
    "720p60",
    "1080p60",
    "1440p60",
    "2160p60",
]

mediaQualities = audioQualities + videoQualities
"""Both audio and video qualities"""

audioBitrates = (
    "64k",
    "96k",
    "128k",
    "192k",
    "256k",
    "320k",
)
"""Audio birates"""

audioBitratesType = t.Literal[
    "64k",
    "96k",
    "128k",
    "192k",
    "256k",
    "320k",
]
