"""Non-changing variables across the package"""

import typing as t

videoExtensionsType = t.Literal["mp4", "webm"]
audioExtensionsType = t.Literal["m4a", "webm"]

videoExtensions: tuple[videoExtensionsType] = ("mp4", "webm")
audioExtensions: tuple[audioExtensionsType] = ("m4a", "webm")

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

videoQualities: tuple[videoQualitiesType] = (
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

audioQualitiesType = t.Literal[
    "ultralow",
    "low",
    "medium",
]

audioQualities: tuple[audioQualitiesType] = (
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

mediaQualities: tuple[mediaQualitiesType] = audioQualities + videoQualities
"""Both audio and video qualities"""

audioBitratesType = t.Literal[
    "64k",
    "96k",
    "128k",
    "192k",
    "256k",
    "320k",
]

audioBitrates: tuple[audioBitratesType] = (
    "64k",
    "96k",
    "128k",
    "192k",
    "256k",
    "320k",
)
"""Audio bitrates"""

video_audio_quality_map: dict[videoQualitiesType, audioQualitiesType] = {
    "144p": "ultralow",
    "240p": "low",
    "360p": "medium",
    "480p": "medium",
    "720p": "medium",
    "1080p": "medium",
    "1440p": "medium",
    "2160p": "medium",
    "720p50": "medium",
    "1080p50": "medium",
    "1440p50": "medium",
    "2160p50": "medium",
    "720p60": "medium",
    "1080p60": "medium",
    "1440p60": "medium",
    "2160p60": "medium",
}
